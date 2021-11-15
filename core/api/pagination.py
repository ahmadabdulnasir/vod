from rest_framework import pagination

class CorePagination(pagination.PageNumberPagination):
	"""Allow DRF Page Pagination"""
	page_size = 100
	page_size_query_param = 'page_size'
	# max_page_size = 1000
	


