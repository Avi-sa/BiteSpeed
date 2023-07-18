from itertools import count
from sys import flags
from rest_framework.response import Response
from customers.models import Contacts
from rest_framework import generics
from django.db.models import Q

# Create your views here.


class IdentifyAPIView(generics.GenericAPIView):
    """For tracking campaign conversions"""

    http_method_names = ["post"]

    def post(self, request):

        try:
            email = request.data.get("email", None)
            phoneNumber = request.data.get("phoneNumber", None)
        except Exception:
            return Response({"msg": "phone number or email not found!"}, status=500)

        if not email and not phoneNumber:
            return Response({"msg": "please pass the valid request args!"}, status=500)

        else:
            contacts = Contacts.objects.filter(
                Q(email=email) | Q(mobile=phoneNumber)
            )

            print('contacts - ', contacts.values())

            primaryUsers = contacts.filter(
                linkPrecidence="primary").values_list("id", flat=True)

            print('contacts - ', primaryUsers)

            if not contacts.count():
                Contacts.objects.create(
                    email=email,
                    mobile=phoneNumber,
                    linkedId=None,
                    linkPrecidence="primary"
                )
                print(1)

            elif contacts.count() > 1 and len(primaryUsers) == contacts.count():
                oldest_id = contacts.order_by("-created_at").first().id
                contacts.filter(~Q(id__in=oldest_id)).update(linkPrecidence="secondary",
                                                             linkedId=oldest_id)

                print(2)

            elif primaryUsers and not contacts.filter(email=email, mobile=phoneNumber).count():
                Contacts.objects.create(
                    email=email,
                    mobile=phoneNumber,
                    linkedId_id=primaryUsers.first(),
                    linkPrecidence="secondary"
                )

                print(3)

            contacts = Contacts.objects.filter(
                Q(email=email) | Q(mobile=phoneNumber)
            )

            primaryUsers = contacts.filter(
                linkPrecidence="primary").values_list("id", flat=True)

            secondaryUsers = contacts.filter(
                ~Q(id__in=primaryUsers)).values_list("id", flat=True)

            response = {
                "contact": {
                    "primaryContatctId": primaryUsers.first() if primaryUsers.count() else 0,
                    "secondaryContactIds": secondaryUsers,
                    "emails": set(contacts.values_list("email", flat=True)),
                    "phoneNumbers": set(contacts.values_list("mobile", flat=True))
                }
            }

            return Response(response, status=200)
