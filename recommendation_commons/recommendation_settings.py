
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from drf_yasg.utils import swagger_auto_schema

from recommendation_commons.serializers import RecommendationSettingsSerializerForDocs
from mec_energia.settings import RECOMMENDATION_METHOD, MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION, IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION, MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_RENOVATION

class RecommendationSettings(ViewSet):
    http_method_names = ['get']

    @swagger_auto_schema(responses={200: RecommendationSettingsSerializerForDocs()})
    def list(self, _):
        settings = {
            'MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION': MINIMUM_ENERGY_BILLS_FOR_RECOMMENDATION,
            'IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION': IDEAL_ENERGY_BILLS_FOR_RECOMMENDATION,
            'MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_RENOVATION': MINIMUM_PERCENTAGE_DIFFERENCE_FOR_CONTRACT_RENOVATION,
            'METHOD': RECOMMENDATION_METHOD
        }

        return Response(settings)
