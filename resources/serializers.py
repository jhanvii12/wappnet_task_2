from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ResourceAllocation, Resource
from psycopg2.extras import DateRange
from datetime import datetime

User = get_user_model()

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'resource_type', 'project', 'total_quantity']

class ResourceAllocationSerializer(serializers.ModelSerializer):
    # Custom field for allocation_period to handle list of dates
    allocation_period = serializers.ListField(
        child=serializers.DateField(),
        write_only=True,
        min_length=2,
        max_length=2,
        help_text="A list of two dates in 'YYYY-MM-DD' format: [start_date, end_date]"
    )

    class Meta:
        model = ResourceAllocation
        fields = ['id', 'resource_type', 'project', 'task', 'allocated_quantity', 'allocation_period']
        read_only_fields = ['id']

    def to_internal_value(self, data):
        # Convert the list of date strings to a DateRange object
        validated_data = super().to_internal_value(data)

        # Handle allocation_period
        if 'allocation_period' in data:
            period = data['allocation_period']
            if not isinstance(period, list) or len(period) != 2:
                raise serializers.ValidationError(
                    {"allocation_period": "Must be a list of two dates: [start_date, end_date]"}
                )

            try:
                start_date = datetime.strptime(period[0], "%Y-%m-%d").date()
                end_date = datetime.strptime(period[1], "%Y-%m-%d").date()
                validated_data['allocation_period'] = DateRange(start_date, end_date, '[)')
            except ValueError as e:
                raise serializers.ValidationError(
                    {"allocation_period": f"Invalid date range: {str(e)}"}
                )

        return validated_data

    def to_representation(self, instance):
        # Convert DateRange back to a list of strings for the response
        data = super().to_representation(instance)
        if isinstance(instance.allocation_period, DateRange):
            data['allocation_period'] = [
                instance.allocation_period.lower.strftime("%Y-%m-%d") if instance.allocation_period.lower else None,
                instance.allocation_period.upper.strftime("%Y-%m-%d") if instance.allocation_period.upper else None
            ]
        return data

    def create(self, validated_data):
        return ResourceAllocation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.resource_type = validated_data.get('resource_type', instance.resource_type)
        instance.project = validated_data.get('project', instance.project)
        instance.task = validated_data.get('task', instance.task)
        instance.allocated_quantity = validated_data.get('allocated_quantity', instance.allocated_quantity)
        instance.allocation_period = validated_data.get('allocation_period', instance.allocation_period)
        instance.save()
        return instance

class ResourceSummarySerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    project_name = serializers.CharField(source='project.name')
    resource_type = serializers.CharField()
    total_quantity = serializers.IntegerField()
    allocated_quantity = serializers.IntegerField()
    available_quantity = serializers.IntegerField()