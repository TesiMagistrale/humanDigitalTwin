
from stereotypes.ftd.sub_domain.ports.MessageOutputPort import MessageOutputPort
from stereotypes.ftd.sub_domain.ports.StereotypePort import StereotypePort
from stereotypes.classes.age_sereotype_class import drive_age_weight
from stereotypes.classes.experience_stereotype_class import drive_experience_and_frequence_weight
from datetime import datetime

from domain.model import PersonService


class FtDStereotypeModule(StereotypePort):
    
    CD = "cognitive_distraction"
    VD = "visual_distraction"
    E = "emotions"
    A = "arousal"
    
    def __init__(self, person_service:PersonService, ftd_calculator: MessageOutputPort, output_comm: MessageOutputPort):
        self.person_service = person_service
        self.ftd_calculator = ftd_calculator
        self.output_comm = output_comm
        
        #initialize module variables
        self.start_drive_km = 0
        self.end_drive_km = 0
        self.yearly_km = 0
        
        self._reset_variables()
    
    
    def compute_data(self, data):
        '''
        TODO: devo gestire i buffer e al momento del calcolo inviare un messaggio al servizio FTD, ottenuto il dato lo ritorno al servizio che lo ritorna all'adapter mqtt e che lo invierà poi alla macchina
        per i km annui salva ogni giorno sul db (ad ogni guida aggiorni il valore del giorno se presente, altrimenti lo crei nuovo con il dato), al momento dell'avvio della guida reperisci il dato aggregato dal db e assegnalo alla variabile yearly_km il dato si riferisce ai km annui rilevati al giorno precedente.
        '''
        
        #update local variables
        sensor_type = data["type"]
        
        
        match sensor_type:
            case self.CD:
                self.cognitive_distraction = data[self.CD]
                self.compute_ftd_flag = True
            case self.VD:
                self.visual_distraction = data[self.VD]
            case self.E:
                for k, v in data[self.E]:
                    self.emotion_arousals_buffer[k] = v
            case self.A:
                self.emotion_arousals_buffer[self.A] = data[self.a]
            case _:
                raise ValueError("wrong sensor type")
            
        if self.compute_ftd_flag:
            self._compute_ftd()
        
        return  
    
    def new_elaborated_data(self, data):
        #send to car the computed data
        print(data)
        self.output_comm.send(data)
        

    def start_module(self, data):
        self.start_drive_km = data["km"]
        self.end_drive_km = 0
        #self.yearly_km = retrive from db from today date and today date - 1 year TODO
        self.person_service.add_actual_state("yearly_km", self.yearly_km)
        self._add_module_state()
        self._reset_variables()
        
    def stop_module(self, data):
        self.end_drive_km = data["km"]
        #TODO save driven km self.service.save(data) ?? da elaborare 
        self._remove_module_state()
        pass
    
    def _reset_variables(self):
        self.emotion_arousals_buffer={
            "anger": [0,0,0,0],
            "happiness" : [0,0,0,0],
            "fear" : [0,0,0,0],
            "sadness" : [0,0,0,0],
            "neutral" : [0,0,0,0],
            "disgust" : [0,0,0,0],
            "surprise" : [0,0,0,0],
            "arousal" : [0, 0, 0, 0],
        }
        self.speed_buffer = [0, 0, 0, 0]
        self.cognitive_distraction = 0
        self.visual_distraction = 0
        self.compute_ftd_flag = False
    
    def _compute_licence_year(self,licence_date):
        today = datetime.today()
        licence_date = datetime.strptime(licence_date, '%Y-%m-%d')
        return today.year - licence_date.year - ((today.month, today.day) < (licence_date.month, licence_date.day))
    
    def _compute_ftd(self):
        age_weight = drive_age_weight(self.person_service.get_age())
        person_general_data = self.person_service.get_general_data()
        
        freq_and_exp_weight = drive_experience_and_frequence_weight(
            licence_year=self._compute_licence_year(person_general_data["licence_date"]),
            yearly_km = self.yearly_km
            )
        
        data = {} #all data
        
        compute_ftd_flag = False
        
    def _add_module_state(self):
        self.person_service.add_actual_state(self.CD, 0)
        self.person_service.add_actual_state(self.VD, 0)
        self.person_service.add_actual_state(self.E, {})
        self.person_service.add_actual_state(self.A, 0)
        self.person_service.add_actual_state("yearly_km", 0)
        self.person_service.add_actual_state("ftd", 1)
        
    def _remove_module_state(self):
        self.person_service.remove_state(self.CD)
        self.person_service.remove_state(self.VD)
        self.person_service.remove_state(self.E)
        self.person_service.remove_state(self.A)
        self.person_service.remove_state("yearly_km")
        self.person_service.remove_state("ftd")
        
    

