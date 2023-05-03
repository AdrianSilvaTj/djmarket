#
from django.db.models import Prefetch, F, FloatField, ExpressionWrapper
#
from applications.venta.models import Sale, SaleDetail


def detalle_ventas_no_cerradas():
    # recuepramos arry de id de ventas no cerradas
    ventas = Sale.objects.ventas_no_cerradas()
    #.prefetch_related, realiza una subconsulta a cada uno de los elementos del queryset de ventas.

    consulta = ventas.prefetch_related(
        Prefetch(
            # en 'detail_sale', es el related_name de la foreign key, se guarda una lista con los SaleDetail, 
            'detail_sale', 
            # hace una consulta filtrando los detalles de ventas que tienen esas ventas y agrega un campo
            # virtual donde calcula el subtotal del renglon de cada detalle
            # output_field=FloatField(), se utiliza para indicar que el resultado sera de tipo decimal
            queryset=SaleDetail.objects.filter(sale__id__in=ventas).annotate(
                subtotal=ExpressionWrapper(
                    F('price_sale')*F('count'),
                    output_field=FloatField()
                )
            )
        )
    )

    return consulta
    