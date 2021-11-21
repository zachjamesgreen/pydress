import factory

import models

class PersonFactory(factory.Factory):
    class Meta:
        model = models.Person
    name = factory.Faker('name')