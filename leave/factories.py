# coding=utf-8
import factory
import faker

from website.factories import UserFactory

from . import models

fake = faker.Faker()


class LeaveRequestFactory(factory.DjangoModelFactory):
    start = factory.Faker("future_date")
    end = factory.Faker("date_between", start_date="+31d", end_date="+180d")
    manager = factory.SubFactory(UserFactory)
    request_by = factory.SubFactory(
        UserFactory, manager=factory.SelfAttribute("..manager")
    )

    class Meta:
        model = models.LeaveRequest
