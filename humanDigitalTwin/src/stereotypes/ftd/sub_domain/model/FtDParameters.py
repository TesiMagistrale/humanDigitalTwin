from enum import Enum, auto

class FtDParameters(Enum):
    CD = ("cd", "cognitive_distraction", "NP_UNITO_DCDC")
    VD = ("vd", "visual_distraction", "AITEK_EVENTS")
    E = ("e", "emotions", "Emotions")
    A = ("a", "arousal", "NP_UNIPR_AROUSAL")
    SPEED = ("speed", "speed", "RL_VehicleDynamics")
    AGE = ("age", "age", "")
    DF = ("df","frequence_exeprience", "")

    def __new__(cls, short_code, full_name, topic):
        obj = object.__new__(cls)
        obj._value_ = short_code
        obj.full_name = full_name
        obj.topic = topic
        return obj

    def __str__(self):
        return f"{self.full_name} ({self.value})"
    
    def get_full_name_from_topic(topic):
        for enum_member in FtDParameters:
            if enum_member.topic == topic:
                return enum_member.full_name