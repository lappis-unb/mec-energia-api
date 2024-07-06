from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from global_search_recommendation.domain import Domain
from global_search_recommendation.runner import PSORunner

class GlobalSearchRecommendationViewSet(ViewSet):
    http_method_names = ['get']

    def retrieve(self, request: Request, pk = None):
        '''Recomendação via busca global. Deve ser fornecido o ID da Unidade Consumidora.'''
        
        domain = Domain(pk)
        domain_mount_result = domain.mount()
        if domain_mount_result:
            return Response(domain_mount_result)
        runner = PSORunner(domain)
        recomendation = runner.calculate()

        return recomendation.build_response()
