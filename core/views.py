from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from django.utils import timezone

# Vendor views
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_list_create(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_retrieve(request, pk):
    try:
        vendor = Vendor.objects.get(pk=pk)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_update(request, pk):
    try:
        vendor = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = VendorSerializer(vendor, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_delete(request, pk):
    try:
        vendor = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    vendor.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Purchase Order views
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_order_list_create(request):
    if request.method == 'GET':
        purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_order_retrieve(request, pk):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=pk)
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_order_update(request, pk):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=pk)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def purchase_order_delete(request, pk):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=pk)
    except PurchaseOrder.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    purchase_order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Historical Performance views
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def historical_performance_list_create(request):
    if request.method == 'GET':
        historical_performance = HistoricalPerformance.objects.all()
        serializer = HistoricalPerformanceSerializer(historical_performance, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = HistoricalPerformanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def historical_performance_retrieve_update_destroy(request, pk):
    try:
        historical_performance = HistoricalPerformance.objects.get(pk=pk)
    except HistoricalPerformance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HistoricalPerformanceSerializer(historical_performance)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = HistoricalPerformanceSerializer(historical_performance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        historical_performance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Backend Logic for Performance Metrics
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    # Calculate performance metrics
    completed_orders = vendor.purchase_orders.filter(status='completed')
    total_completed_orders = completed_orders.count()

    on_time_orders = completed_orders.filter(delivery_date__lte=timezone.now())
    on_time_delivery_rate = on_time_orders.count() / total_completed_orders if total_completed_orders > 0 else 0

    quality_ratings = completed_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
    quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if len(quality_ratings) > 0 else 0

    acknowledged_orders = completed_orders.exclude(acknowledgment__isnull=True)
    response_times = [(po.acknowledgment - po.issue_date).total_seconds() / 60 for po in acknowledged_orders]
    average_response_time = sum(response_times) / len(response_times) if len(response_times) > 0 else 0

    successful_orders = completed_orders.exclude(status='completed_with_issues')
    fulfillment_rate = successful_orders.count() / vendor.purchase_orders.count() if vendor.purchase_orders.count() > 0 else 0

    # Prepare response
    performance_data = {
        "on_time_delivery_rate": on_time_delivery_rate,
        "quality_rating_avg": quality_rating_avg,
        "average_response_time": average_response_time,
        "fulfillment_rate": fulfillment_rate
    }

    return Response(performance_data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def acknowledge_purchase_order(request, po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

    # Update acknowledgment date
    purchase_order.acknowledgment = timezone.now()
    purchase_order.save()

    # Trigger recalculation of average_response_time for the vendor
    vendor = purchase_order.vendor
    acknowledged_orders = vendor.purchase_orders.exclude(acknowledgment__isnull=True)
    response_times = [(po.acknowledgment - po.issue_date).total_seconds() / 60 for po in acknowledged_orders]
    average_response_time = sum(response_times) / len(response_times) if len(response_times) > 0 else 0
    vendor.average_response_time = average_response_time
    vendor.save()

    return Response({"message": "Purchase order acknowledged successfully"})