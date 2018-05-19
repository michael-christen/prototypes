from schematics.models import Model
from schematics.types import StringType, FloatType, PolyModelType


class Man(Model):
    type = StringType(required=True, choices=('man',), default='man')
    arm_strength = FloatType(required=True)

    @classmethod
    def _claim_polymorphic(cls, data):
        return data.get('type') == 'man'


class Woman(Model):
    type = StringType(required=True, choices=('woman',), default='woman')
    emotional_strength = FloatType(required=True)

    @classmethod
    def _claim_polymorphic(cls, data):
        return data.get('type') == 'woman'


class PersonParser(Model):
    person = PolyModelType((Man, Woman))


class Somebody(object):
    def __init__(self, obj_dict):
        person_parser = PersonParser(dict(person=obj_dict))
        person_parser.validate()
        self.person = person_parser.person

    def get_person(self):
        return self.person


def main():
    man = Somebody({
        'type': 'man',
        'arm_strength': 12.3,
    }).get_person()
    man.validate()
    print(man)
    woman = Somebody({
        'type': 'woman',
        'emotional_strength': 4.3,
    }).get_person()
    woman.validate()
    print(woman)


if __name__ == '__main__':
    main()
