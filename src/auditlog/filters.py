from django.contrib.admin import SimpleListFilter


class ResourceTypeFilter(SimpleListFilter):
    title = 'Resource Type'
    parameter_name = 'resource_type'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        types = qs.values_list('content_type_id', 'content_type__model')
        return list(types.order_by('content_type__model').distinct())

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(content_type_id=self.value())


class UserTypeFilter(SimpleListFilter):
    title = 'User'
    parameter_name = 'user'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        types = qs.values_list('actor_id', 'actor__username')
        print 'UserTypeFilter'
        print types
        return list(types.order_by('actor__username').distinct())

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(actor_id=self.value())


class CustomerTypeFilter(SimpleListFilter):
    title = 'Customer'
    parameter_name = 'customer'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request).filter(content_type__model='customer')
        types = qs.values_list('object_pk', 'object_repr')
        return list(types.order_by('object_repr').distinct())

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        qs_customer = queryset.filter(object_pk=self.value())
        qs_session = queryset.filter(related_object_pk=self.value())
        qs = qs_customer | qs_session
        return qs


class StudentTypeFilter(SimpleListFilter):
    title = 'Student'
    parameter_name = 'student'

    def lookups(self, request, model_admin):
        qs_student = model_admin.get_queryset(request).filter(content_type__model='student')
        types_student = qs_student.values_list('object_pk', 'object_repr')
        return list(types_student.order_by('object_repr').distinct())

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        qs_student = queryset.filter(object_pk=self.value())
        qs_session = queryset.filter(related_object_pk=self.value())
        qs = qs_student | qs_session
        return qs
