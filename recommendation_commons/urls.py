from rest_framework.routers import DefaultRouter
from recommendation.views import RecommendationViewSet
from recommendation_commons.recommendation_settings import RecommendationSettings
from global_search_recommendation.views import GlobalSearchRecommendationViewSet
from mec_energia.settings import RECOMMENDATION_METHOD, ENVIRONMENT

router = DefaultRouter()

router.register(r'recommendation', GlobalSearchRecommendationViewSet if RECOMMENDATION_METHOD in ['pso', 'ga'] else RecommendationViewSet, basename='recommendation')
router.register(r'recommendation-settings', RecommendationSettings, basename='recommendation-settings')

if(ENVIRONMENT != 'production'):
    router.register(r'global-search-recommendation', GlobalSearchRecommendationViewSet, basename='global-search-recommendation')
    router.register(r'percentile-recommendation', RecommendationViewSet, basename='percentile-recommendation')

