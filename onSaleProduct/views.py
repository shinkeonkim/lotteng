from django.http import response
from django.shortcuts import get_object_or_404, render
from .models import OnSaleProduct
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta

DEFAULT_PAGE_CNT = 10 # 한 페이지에 있는 상품의 기본 개수 
PAGE_NAV_LEFT = 5 # pageination nav bar의 왼쪽 넘버링 개수
PAGE_NAV_RIGHT = 5 # pageination nav bar의 오른쪽 넘버링 개수

'''
request로 들어오는 문자열이 정당한 경우, int 로 변환
아닌 경우, default 값을 return 하는 함수 
'''
def requestStrToInt(str, defalut = 1):
    ret = defalut
    try:
        ret = int(str)
    except:
        ret = defalut
    return ret

'''
시장 철수, 할인 마감등이 되지 않은 할인 중인 상품 목록을 return하는 뷰
'''
def show_on_sale_product_list(request):
    # request content
    page = requestStrToInt(request.GET.get('page')) # page 넘버
    page_cnt = requestStrToInt(request.GET.get('page_cnt', DEFAULT_PAGE_CNT)) # 한 페이지에 있는 상품의 수, defalt = 10

    # query
    time_threshold = datetime.now()

    on_sale_products = OnSaleProduct.objects.all()
    on_sale_products = on_sale_products.filter(endDate__gt=time_threshold, stock__gt = 0) # 상품이 시장 철수를 하였거나, 할인이 마감된 할인 상품은 배제한다.
    on_sale_products = on_sale_products[::-1] # 최근에 등록된 상품이 앞으로 오게 한다.

    # pagination
    paginator = Paginator(on_sale_products, page_cnt)
    on_sale_products_current_page = paginator.get_page(page)

    # pagination nav bar range
    start = max(int(page)-PAGE_NAV_LEFT, 1)
    end = min(int(page)+PAGE_NAV_RIGHT, paginator.num_pages)

    return render(request, 'show_on_sale_product_list.html',\
        {
            'on_sale_products_current_page': on_sale_products_current_page,
            'page': page, 
            'page_cnt': page_cnt, 
            'range' : [i for i in range(start, end+1)]
        })

'''
시장 철수, 할인 마감등이 되지 않은 할인 중인 상품 목록을 
다른 페이지에서 사용하기 위한 함수
'''
def get_on_sale_product_list(page, page_cnt):
    # query
    time_threshold = datetime.now()

    on_sale_products = OnSaleProduct.objects.all()
    on_sale_products = on_sale_products.filter(endDate__gt=time_threshold, stock__gt = 0) # 상품이 시장 철수를 하였거나, 할인이 마감된 할인 상품은 배제한다.
    on_sale_products = on_sale_products[::-1] # 최근에 등록된 상품이 앞으로 오게 한다.

    # pagination
    paginator = Paginator(on_sale_products, page_cnt)
    on_sale_products_current_page = paginator.get_page(page)

    # pagination nav bar range
    start = max(int(page)-PAGE_NAV_LEFT, 1)
    end = min(int(page)+PAGE_NAV_RIGHT, paginator.num_pages)

    return {
        'on_sale_products_current_page': on_sale_products_current_page,
        'page': page, 
        'page_cnt': page_cnt, 
        'range' : [i for i in range(start, end+1)]
    }

'''
시장 철수, 할인 마감등이 되지 않은 할인 중인 상품인 경우에만 상품 정보 뷰를 return
아닌 경우, is_not_on_sale_product.html을 404 status로 return
'''
def show_on_sale_product_detail(request, id):
    product = get_object_or_404(OnSaleProduct, pk = id)

    # 할인 시간이 지난 경우의 상품의 detail 페이지를 요구하는 경우
    if product.endDate < datetime.now() or product.stock <= 0:
        response = render(request, "is_not_on_sale_product.html")
        response.status_code = 404
        return response

    return render(request, 'show_on_sale_product_detail.html',\
        {
            'product': product,
        }
    )

'''
시장 철수, 할인 마감등이 되지 않은 할인 중인 상품을 
다른 페이지에서 사용하기 위한 함수
'''
def get_on_sale_product_detail():
    product = get_object_or_404(OnSaleProduct, pk = id)

    # 할인 시간이 지난 경우의 상품의 detail 페이지를 요구하는 경우
    if product.endDate < datetime.now():
        return None

    return {
        'product': product,
    }