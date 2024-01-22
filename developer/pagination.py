# from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response


# class ProjectViewPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = 'page_size'
#     max_page_size = 1000

#     def get_paginated_response(self, data):
#         return Response({
#             'links': {
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link()
#             },
#             'count': self.page.paginator.count,
#             'page_size': self.page_size,
#             'results': data
#         })