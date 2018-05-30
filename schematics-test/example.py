from schematics.models import Model
from schematics.types import StringType, FloatType, PolyModelType


class PolymorphicID(StringType):
    """Add this type to a class to allow it to work w/ ClaimPolyModelType

    ClaimPolyModelType recognizes these types and looks for the identifier
    specified. These types also automatically ensure that the value is always
    set to the identifier by restricting choices.
    """
    def __init__(self, identifier, *args, **kwargs):
        self.identifier = identifier
        new_kwargs = dict(
            required=True,
            choices=(identifier,),
            default=identifier,
        )
        for arg in new_kwargs:
            if arg in kwargs:
                raise AssertionError("{} not allowed in __init__ of {}"
                                     .format(arg, self.__class__.__name__))
        kwargs.update(new_kwargs)
        super(PolymorphicID, self).__init__(*args, **kwargs)


def _generate_claim_function(models):
    """Return a function that evaluates the data to determine which of the
    models to return.

    Looks for a PolymorphicID in each of the models, and ensures there is only
    one.
    """
    polymorphic_field_name = None
    field_value2model = {}
    # Define a mapping of type to model
    for model in models:
        polymorphic_field_value = None
        for field_name, field_type in model.fields.items():
            if isinstance(field_type, PolymorphicID):
                if polymorphic_field_name is None:
                    polymorphic_field_name = field_name
                else:
                    assert polymorphic_field_name == field_name, (
                        "Multiple polymorphic field names in between Models")
                if polymorphic_field_value is None:
                    polymorphic_field_value = field_type.identifier
                else:
                    raise AssertionError(
                        "Got multiple polymorphicIDs in a Model")
        if polymorphic_field_value is None:
            raise AssertionError("No polymorphicID found for model: {}"
                                 .format(model))
        existing_model = field_value2model.get(polymorphic_field_value)
        if existing_model:
            raise AssertionError("Duplicate polymorphicIDs found with value "
                                 "{}.  {} & {}".format(polymorphic_field_value,
                                                       existing_model, model))
        field_value2model[polymorphic_field_value] = model

    def _claim_function(polymodel, data):
        """Return the class that corresponds to this data."""
        try:
            value = data[polymorphic_field_name]
        except KeyError:
            raise AssertionError("Data should have {}. {}"
                                 .format(polymorphic_field_name, data))
        try:
            return field_value2model[value]
        except KeyError:
            raise AssertionError("None of these models {} match {}"
                                 .format(models, value))

    return _claim_function


class ClaimPolyModelType(PolyModelType):
    """Extend PolyModelType to set up the claim_function automatically

    This allows for the use of specific identifiers defined with a
    PolymorphicID, that specify which model to use. All of the field names must
    be the same between polymorphic models.
    """
    def __init__(self, model_spec, *args, **kwargs):
        new_kwargs = dict(
            claim_function=_generate_claim_function(model_spec),
        )
        # Check that not conflicting with kwargs
        for arg in new_kwargs:
            if arg in kwargs:
                raise AssertionError("{} not allowed in __init__ of {}"
                                     .format(arg, self.__class__.__name__))
        kwargs.update(new_kwargs)
        super(ClaimPolyModelType, self).__init__(model_spec, *args, **kwargs)


class Man(Model):
    type = PolymorphicID('man')
    arm_strength = FloatType(required=True)


class Woman(Model):
    type = PolymorphicID('woman')
    emotional_strength = FloatType(required=True)


class PersonParser(Model):
    person = ClaimPolyModelType((Man, Woman))


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
