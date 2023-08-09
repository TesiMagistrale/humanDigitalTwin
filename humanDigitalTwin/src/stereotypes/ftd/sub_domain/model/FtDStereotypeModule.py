
import numpy as np
from stereotypes.ftd.sub_domain.ports.MessageOutputPort import MessageOutputPort
from stereotypes.ftd.sub_domain.ports.StereotypePort import StereotypePort
from stereotypes.ftd.sub_domain.model.FtDParameters import FtDParameters
from stereotypes.classes.age_sereotype_class import drive_age_weight
from stereotypes.classes.experience_stereotype_class import drive_experience_and_frequence_weight
from datetime import datetime

from domain.model import PersonService


class FtDStereotypeModule(StereotypePort):
    
    def __init__(self, person_service:PersonService, ftd_calculator: MessageOutputPort, output_comm: MessageOutputPort):
        self.person_service = person_service
        self.ftd_calculator = ftd_calculator
        self.output_comm = output_comm
        
        #initialize module variables
        self.start_drive_km = 0
        FtDParameters.E.full_namend_drive_km = 0
        self.yearly_km = 0
        
        self._reset_variables()
    
    
    async def compute_data(self, data):
        '''
        TODO: devo gestire i buffer e al momento del calcolo inviare un messaggio al servizio FTD, ottenuto il dato lo ritorno al servizio che lo ritorna all'adapter mqtt e che lo invierà poi alla macchina
        per i km annui salva ogni giorno sul db (ad ogni guida aggiorni il valore del giorno se presente, altrimenti lo crei nuovo con il dato), al momento dell'avvio della guida reperisci il dato aggregato dal db e assegnalo alla variabile yearly_km il dato si riferisce ai km annui rilevati al giorno precedente.
        '''
        
        #update local variables
        sensor_type = data["type"]
        #TODO update sensor_actual value
        match sensor_type:
            case FtDParameters.CD.full_name:
                '''
                data[FtDParameters.CD.full_name]= {
                    sensor_value: X,
                    timestamp: timestamp
                }
                '''
                self.cognitive_distraction = data[FtDParameters.CD.full_name]
                self.compute_ftd_flag = True
            case FtDParameters.VD.full_name:
                '''
                data[FtDParameters.VD.full_name]= {
                    sensor_value: X,
                    timestamp: timestamp
                }
                '''
                self.visual_distraction = data[FtDParameters.VD.full_name]
            case FtDParameters.E.full_name:
                '''
                data[FtDParameters.E.full_name]= {"anger": 0.45699999999999996, "happiness": 0.01895, "fear": 0.0030499999999999998, "sadness": 0.00065, "neutral": 0.0024, "disgust": 0.013025, "surprise": 0.004925}
                '''
                for k,v in data[FtDParameters.E.full_name].items():
                    buffer = self.emotion_buffer[k]
                    buffer.pop()
                    buffer.append(float(v))
            case FtDParameters.A.full_name:
                '''
                data[FtDParameters.Afull_name]= 0.1
                '''
                self.arousal_buffer.pop(0)
                self.arousal_buffer.append(float(data[FtDParameters.A.full_name]))
            case FtDParameters.SPEED.full_name:
                '''
                data[FtDParameters.SPEED.full_name]= 100
                '''
                self.speed_buffer.pop(0)
                self.speed_buffer.append(float(data[FtDParameters.SPEED.full_name]))
            case _:
                raise ValueError("wrong sensor type")
            
        if self.compute_ftd_flag:
            await self._compute_ftd()
        
        return  
    
    async def new_elaborated_data(self, data):
        self.person_service.update_actual_state("ftd", data["ftd"])
        await self.output_comm.send(data)
        

    def start(self, data):
        self.start_drive_km = data["km"]
        self.end_drive_km = 0
        #self.yearly_km = retrive from db from today date and today date - 1 year TODO
        self.yearly_km = 5000
        self.person_service.add_actual_state("yearly_km", self.yearly_km)
        self._add_module_state()
        self._reset_variables()
        
    def stop(self, data):
        self.end_drive_km = data["km"]
        #TODO save driven km self.service.save(data) ?? da elaborare 
        self._remove_module_state()
    
    def _reset_variables(self):
        self.emotion_buffer={
            "anger": [0,0,0,0],
            "happiness" : [0,0,0,0],
            "fear" : [0,0,0,0],
            "sadness" : [0,0,0,0],
            "neutral" : [0,0,0,0],
            "disgust" : [0,0,0,0],
            "surprise" : [0,0,0,0],
        }
        self.arousal_buffer = [0, 0, 0, 0]
        self.speed_buffer = [0, 0, 0, 0]
        self.cognitive_distraction = {
            "sensor_value": 0,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "speed": 0
        }
        self.visual_distraction = {
            "sensor_value": 0,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "speed": 0
        }
        self.compute_ftd_flag = False
    
    def _compute_licence_year(self,licence_date):
        today = datetime.today()
        licence_date = datetime.strptime(licence_date, '%Y-%m-%d')
        return today.year - licence_date.year - ((today.month, today.day) < (licence_date.month, licence_date.day))
    
    async def _compute_ftd(self):
        age_weight = drive_age_weight(self.person_service.get_age())
        person_general_data = self.person_service.get_general_data()
        
        freq_and_exp_weight = drive_experience_and_frequence_weight(
            licence_year=self._compute_licence_year(person_general_data["licence_date"]),
            yearly_km = self.yearly_km
            )
        
        #the structure of the message is established before with and adere to the service that calculate the FTD
        speed_mean = np.mean(self.speed_buffer)
        emotion_mean = {}
        for k, v in self.emotion_buffer.items():
            emotion_mean[k] = np.mean(v)
            
        data = {
            "person_id": person_general_data["id"],
            FtDParameters.CD.value: {
                "sensor_value": int(self.cognitive_distraction["sensor_value"]),
                "timestamp": self.cognitive_distraction["timestamp"],
                "speed": speed_mean
                },
            FtDParameters.VD.value: {
                "sensor_value": int(self.visual_distraction["sensor_value"]),
                "timestamp": self.visual_distraction["timestamp"],
                "speed": speed_mean
                },
            FtDParameters.E.value + "" + FtDParameters.A.value: {
                "timestamp": int(datetime.now().timestamp() * 1000), 
                "emotion_sensor":  emotion_mean,
                "arousal_sensor": np.mean(self.arousal_buffer)
                },
            FtDParameters.AGE.value: age_weight,
            FtDParameters.DF.value: freq_and_exp_weight
        }
        
        await self.ftd_calculator.send(data)
        self.compute_ftd_flag = False
        
    def _add_module_state(self):
        self.person_service.add_actual_state(FtDParameters.CD.full_name, 0)
        self.person_service.add_actual_state(FtDParameters.VD.full_name, 0)
        self.person_service.add_actual_state(FtDParameters.E.full_name, {})
        self.person_service.add_actual_state(FtDParameters.A.full_name, 0)
        self.person_service.add_actual_state("yearly_km", 0)
        self.person_service.add_actual_state("ftd", 1)
        
    def _remove_module_state(self):
        self.person_service.remove_state(FtDParameters.CD.full_name)
        self.person_service.remove_state(FtDParameters.VD.full_name)
        self.person_service.remove_state(FtDParameters.E.full_name)
        self.person_service.remove_state(FtDParameters.A.full_name)
        self.person_service.remove_state("yearly_km")
        self.person_service.remove_state("ftd")
        
    #TODO add on off sensor
        
    

