import json


class TransferRequest:
    """
    {
        id: str
        fr: str
        to: str 

        cargo_type: str
        weight: num
        volume: num

        depart_min: Date (str)
        depart_max: Date (str)
    }
    """
    def __init__(self, data=None, **kwargs):
        if data is not None:
            kwargs.update(data)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        return {key: value 
            for key, value in self.__dict__.items() 
            if not key.startswith('_')
        }

