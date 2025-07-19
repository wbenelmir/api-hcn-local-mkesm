from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.safestring import mark_safe
import json

from .models import PostCurrencyRequest, PostMarchandiseRequest

@admin.register(PostCurrencyRequest)
class PostCurrencyRequestAdmin(ImportExportModelAdmin):
    list_display = (
        'code',
        'rstatus',
        'message',
        'status',
        'user',
        'created_at',
        'updated_at',
    )

    readonly_fields = (
        'code',
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
        'rstatus',
        'message',
        'status',
        'user',
        'created_at',
        'updated_at',
    )

    readonly_fields = (
        'code',
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