from django.contrib import admin, messages
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
import json
from django.db.models import Q
from .models import PostCurrencyRequest, PostMarchandiseRequest, GoodsItem, Unit
from decimal import Decimal
from django.contrib import admin, messages



@admin.register(PostCurrencyRequest)
class PostCurrencyRequestAdmin(ImportExportModelAdmin):
    list_display = (
        'code',
        'code_request',
        'rstatus',
        'message',
        'status',
        'user',
        'created_at',
        'updated_at',
    )

    readonly_fields = (
        'code_request',
        'status',
        'rstatus',
        'message',
        'errors',
        'created_at',
        'updated_at',
        'pretty_post_data',
        'pretty_return_data',
        'formatted_return_errors',
        'formatted_return_update',
    )

    search_fields = ('code', 'user__username')
    list_filter = ('active', 'created_at', 'user')

    # def get_message(self, obj):
    #     return obj.return_data.get('message', '-') if obj.return_data else '-'
    # get_message.short_description = 'Message'

    def pretty_post_data(self, obj):
        """Affichage JSON formaté du post_data."""
        if not obj.post_data:
            return "-"
        formatted = json.dumps(obj.post_data, indent=2, ensure_ascii=False)
        return mark_safe(f"<pre style='white-space: pre-wrap'>{formatted}</pre>")
    pretty_post_data.short_description = "Données envoyées (JSON)"

    def pretty_return_data(self, obj):
        """Affichage JSON formaté du return_data."""
        if not obj.return_data:
            return "-"
        formatted = json.dumps(obj.return_data, indent=2, ensure_ascii=False)
        return mark_safe(f"<pre style='white-space: pre-wrap'>{formatted}</pre>")
    pretty_return_data.short_description = "Données retournées (JSON)"

    def formatted_return_errors(self, obj):
        if not obj.errors:
            return "-"
        return mark_safe("<pre>" + json.dumps(obj.errors, indent=2, ensure_ascii=False) + "</pre>")

    formatted_return_errors.short_description = "Erreurs API"

    def formatted_return_update(self, obj):
        if not obj.api_update:
            return "-"
        return mark_safe("<pre>" + json.dumps(obj.api_update, indent=2, ensure_ascii=False) + "</pre>")

    formatted_return_update.short_description = "Update return API"
   
@admin.register(PostMarchandiseRequest)
class PostMarchandiseRequestAdmin(ImportExportModelAdmin):
    list_display = (
        'code',
        'code_request',
        'rstatus',
        'message',
        'status',
        'user',
        'created_at',
        'updated_at',
    )

    readonly_fields = (
        'status',
        'rstatus',
        'message',
        'errors',
        'created_at',
        'updated_at',
        'pretty_post_data',
        'pretty_return_data',
        'formatted_return_errors',
        'formatted_return_update',
    )

    search_fields = ('code', 'user__username')
    list_filter = ('active', 'created_at', 'user')

    # def get_message(self, obj):
    #     return obj.return_data.get('message', '-') if obj.return_data else '-'
    # get_message.short_description = 'Message'

    def pretty_post_data(self, obj):
        """Affichage JSON formaté du post_data."""
        if not obj.post_data:
            return "-"
        formatted = json.dumps(obj.post_data, indent=2, ensure_ascii=False)
        return mark_safe(f"<pre style='white-space: pre-wrap'>{formatted}</pre>")
    pretty_post_data.short_description = "Données envoyées (JSON)"

    def pretty_return_data(self, obj):
        """Affichage JSON formaté du return_data."""
        if not obj.return_data:
            return "-"
        formatted = json.dumps(obj.return_data, indent=2, ensure_ascii=False)
        return mark_safe(f"<pre style='white-space: pre-wrap'>{formatted}</pre>")
    pretty_return_data.short_description = "Données retournées (JSON)"

    def formatted_return_errors(self, obj):
        if not obj.errors:
            return "-"
        return mark_safe("<pre>" + json.dumps(obj.errors, indent=2, ensure_ascii=False) + "</pre>")

    formatted_return_errors.short_description = "Erreurs API"

    def formatted_return_update(self, obj):
        if not obj.api_update:
            return "-"
        return mark_safe("<pre>" + json.dumps(obj.api_update, indent=2, ensure_ascii=False) + "</pre>")

    formatted_return_update.short_description = "Update return API"


@admin.register(Unit)
class UnitAdmin(ImportExportModelAdmin):
    list_display = (
        'code',
        'name_fr',
        'name_ar',
        'base_unit',
        'factor_to_base',
        'is_active',
    )

    readonly_fields = (
        'code',
        'name_fr',
        'name_ar',
        'base_unit',
        'factor_to_base',
        'is_active',

    )



# -------- GoodsItem --------
@admin.register(GoodsItem)
class GoodsItemAdmin(ImportExportModelAdmin):
    date_hierarchy = "created_at"

    # Columns in changelist
    list_display = (
        "code",
        "name",
        "quantity",
        "unit",
        "currency",
        "unit_value_declared",
        "unit_value_dzd",
        "display_total_value_dzd",
        "declaration",
        "active",
        "created_at",
    )
    list_display_links = ("code", "name")

    # Speed up FK display in list by joining Unit
    # list_select_related = ("unit",)

    # Filters
    list_filter = (
        "active",
        "currency",
        "unit",
        ("created_at", admin.DateFieldListFilter),
    )

    # Search bar
    search_fields = ("code", "name", "declaration")

    # Readonly bookkeeping (add pretty json)
    readonly_fields = (
        "created_at",
        "updated_at",
        "display_total_value_dzd",
        "pretty_json_after",
    )

    # Field layout
    fieldsets = (
        (_("Identity & link"), {
            "fields": ("code", "declaration", "active")
        }),
        (_("Goods info"), {
            "fields": (
                "name",
                "quantity",
                "unit",
                "currency",
                "unit_value_declared",
                "unit_value_dzd",
                "display_total_value_dzd",
            )
        }),
        (_("JSON snapshots"), {
            "classes": ("collapse",),
            "fields": ("pretty_json_after",)  # read-only nicely formatted JSON
        }),
        (_("Timestamps"), {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at")
        }),
    )

    # If UnitAdmin has search_fields set, this gives a great UX:
    # autocomplete_fields = ("unit",)

    # Performance
    list_per_page = 50
    ordering = ("-created_at", "id")

    # Computed display (read-only)
    @admin.display(description=_("Total DZD"), ordering="unit_value_dzd")
    def display_total_value_dzd(self, obj: GoodsItem):
        """
        If 'total_value_dzd' is a @property on the model:
        - We can't order by it directly; use 'unit_value_dzd' as a proxy or
          add an annotated column in get_queryset if exact ordering is needed.
        """
        try:
            return f"{obj.total_value_dzd:.3f}"
        except Exception:
            return "-"

    # Nicely formatted JSON for json_after
    @admin.display(description=_("Données retournées (JSON)"))
    def pretty_json_after(self, obj: GoodsItem):
        data = getattr(obj, "json_after", None)
        if not data:
            return "-"
        try:
            formatted = json.dumps(data, indent=2, ensure_ascii=False)
        except (TypeError, ValueError):
            # If it isn't serializable, just show the raw value
            formatted = str(data)
        return mark_safe(f"<pre style='white-space: pre-wrap; max-height: 500px; overflow:auto'>{formatted}</pre>")

    # Bulk actions
    actions = ["mark_active", "mark_inactive"]

    @admin.action(description=_("Mark selected goods as ACTIVE"))
    def mark_active(self, request, queryset):
        updated = queryset.update(active=True)
        self.message_user(request, _("%d item(s) marked active.") % updated, level=messages.SUCCESS)

    @admin.action(description=_("Mark selected goods as INACTIVE"))
    def mark_inactive(self, request, queryset):
        updated = queryset.update(active=False)
        self.message_user(request, _("%d item(s) marked inactive.") % updated, level=messages.SUCCESS)

    # Optional: if you want exact ordering by total value in the list view,
    # you can annotate in get_queryset (assuming total = quantity * unit_value_dzd).
    # def get_queryset(self, request):
    #     qs = super().get_queryset(request).select_related("unit")
    #     return qs.annotate(_total_dzd=F("quantity") * F("unit_value_dzd"))
    # Then set: @admin.display(ordering="_total_dzd") on display_total_value_dzd.