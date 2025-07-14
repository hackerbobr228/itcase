from django.conf import settings
from paymeuz import Payme

payme = Payme(
    merchant_id=settings.PAYME_MERCHANT_ID,
    key=settings.PAYME_KEY,
    test=settings.PAYME_TEST
)
