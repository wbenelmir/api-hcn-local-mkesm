from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import hashlib
import random
from django.core.exceptions import ValidationError
from decimal import Decimal, ROUND_HALF_UP
from django.core.validators import FileExtensionValidator, RegexValidator, MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from typing import Optional, Union
from django.db.models import Q

CUSTOM_ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789' 
ALPHABET_BASE = len(CUSTOM_ALPHABET)
OFFSET = 401 

def _base_n_encode(number: int) -> str:
    if number == 0:
        return CUSTOM_ALPHABET[0]
    result = ''
    while number > 0:
        number, rem = divmod(number, ALPHABET_BASE)
        result = CUSTOM_ALPHABET[rem] + result
    return result

def encode_pk(pk: int, prefix_length: int = 2) -> str:
    obfuscated = pk + OFFSET
    encoded = _base_n_encode(obfuscated)

    # توليد بادئة من SHA256
    hash_val = hashlib.sha256(str(pk).encode()).hexdigest()
    prefix = ''.join(
        CUSTOM_ALPHABET[int(hash_val[i * 2:i * 2 + 2], 16) % ALPHABET_BASE]
        for i in range(prefix_length)
    )

    return prefix + encoded

def decode_code(code: str, prefix_length: int = 2) -> int:
    encoded = code[prefix_length:]
    value = 0
    for char in encoded:
        value = value * ALPHABET_BASE + CUSTOM_ALPHABET.index(char)
    return value - OFFSET

class PostCurrencyRequest(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True,
        editable=True,
        blank=True,
        null=True,
        help_text="Code fourni par l'utilisateur ou par l'application externe"
    )

    code_request = models.CharField(
        max_length=200,
        editable=False,
        blank=True,
        null=True,
        help_text="code_request_from_currencyrequest"
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Utilisateur"
    )

    post_data = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        verbose_name="Données postées"
    )

    return_data = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        verbose_name="Données retournées"
    )

    status = models.CharField(
        max_length=50,
        editable=False,
        blank=True,
        null=True,
        default="pending",
        help_text="Statut de la réponse API"
    )
    
    rstatus = models.CharField(
        max_length=50,
        editable=False,
        blank=True,
        null=True,
        default="Status retourné par l’API"
    )

    message = models.TextField(
        blank=True,
        null=True,
        help_text="Message retourné par l’API"
    )

    errors = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="Liste des erreurs retournées par l’API"
    )

    api_update = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="Updat retournées par l’API"
    )
    
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_code(self):
        today_str = timezone.now().strftime('%y%m%d')
        return f"{today_str}-{encode_pk(self.pk)}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.code:
            self.code = self.generate_code()
            PostCurrencyRequest.objects.filter(pk=self.pk).update(code=self.code)

    def __str__(self):
        return self.code.lower() if self.code else "-"

class PostMarchandiseRequest(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True,
        editable=True,
        blank=True,
        null=True,
        help_text="Code fourni par l'utilisateur ou par l'application externe"
    )

    code_request = models.CharField(
        max_length=200,
        editable=False,
        blank=True,
        null=True,
        help_text="code_request_from_PostMarchandiseRequest"
    )
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Utilisateur"
    )

    post_data = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        verbose_name="Données postées"
    )

    return_data = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        verbose_name="Données retournées"
    )

    status = models.CharField(
        max_length=50,
        editable=False,
        blank=True,
        null=True,
        default="pending",
        help_text="Statut de la réponse API"
    )
    
    rstatus = models.CharField(
        max_length=50,
        editable=False,
        blank=True,
        null=True,
        default="Status retourné par l’API"
    )

    message = models.TextField(
        blank=True,
        null=True,
        help_text="Message retourné par l’API"
    )

    errors = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="Liste des erreurs retournées par l’API"
    )

    api_update = models.JSONField(
        default=dict,
        blank=True,
        null=True,
        help_text="Updat retournées par l’API"
    )
    
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_code(self):
        today_str = timezone.now().strftime('%y%m%d')
        return f"{today_str}-{encode_pk(self.pk)}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and not self.code:
            self.code = self.generate_code()
            PostMarchandiseRequest.objects.filter(pk=self.pk).update(code=self.code)

    def __str__(self):
        return self.code.lower() if self.code else "-"

class Unit(models.Model):
    code = models.CharField(
        max_length=12,
        unique=True,
        help_text=_("Code court (ex.: KG, L, PIECE)."),
        verbose_name=_("Code"),
    )
    name_fr = models.CharField(max_length=100, verbose_name=_("Nom (FR)"))
    name_ar = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Nom (AR)"))

    # Optional normalization/conversion helpers
    base_unit = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="derived_units",
        help_text=_("Unité de base pour la conversion (ex.: KG pour G)."),
        verbose_name=_("Unité de base"),
    )
    factor_to_base = models.DecimalField(
        max_digits=18,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text=_("Multiplicateur vers l’unité de base (ex.: 0.001 pour G → KG)."),
        verbose_name=_("Facteur vers base"),
    )

    is_active = models.BooleanField(default=True, db_index=True, verbose_name=_("Actif"))
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = _("Unité")
        verbose_name_plural = _("Unités")
        ordering = ["code"]
        indexes = [
            models.Index(fields=["code"], name="idx_unit_code"),
            models.Index(fields=["is_active"], name="idx_unit_active"),
        ]
        constraints = [
            # If a unit has a base_unit, it should have a positive factor_to_base
            models.CheckConstraint(
                check=(
                    models.Q(base_unit__isnull=True, factor_to_base__isnull=True) |
                    models.Q(base_unit__isnull=False, factor_to_base__gt=0)
                ),
                name="ck_unit_factor_when_base",
            ),
            # Prevent self-referential base unit
            models.CheckConstraint(
                check=~models.Q(base_unit=models.F("pk")) | models.Q(base_unit__isnull=True),
                name="ck_unit_not_self_base",
            ),
        ]

    def __str__(self):
        label = f"{self.code} {self.name_fr}"
        return f"{label} - {self.name_ar}" if self.name_ar else label

    def clean(self):
        if self.code:
            self.code = self.code.upper().strip()
        # If factor provided, base_unit must be present (and vice versa)
        if (self.base_unit is None) ^ (self.factor_to_base is None):
            from django.core.exceptions import ValidationError
            raise ValidationError(_("Si une conversion est définie, 'base_unit' et 'factor_to_base' doivent être renseignés."))

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
        
class GoodsItem(models.Model):
    code = models.CharField(max_length=200, blank=False, null=False, unique=True)
    declaration = models.CharField(_("Declaration code"), max_length=255, blank=True, null=True)

    name = models.CharField(_("Nom de la marchandise"), max_length=255, blank=True, null=True)
    quantity = models.PositiveIntegerField(_("Quantité"), validators=[MinValueValidator(1)], blank=True, null=True)
    unit = models.CharField(_("unit"), max_length=255, blank=True, null=True)

    # Devise de saisie
    currency = models.CharField(
        _("Devise"),
        max_length=3,
        default="EUR",
        validators=[RegexValidator(r"^[A-Z]{3}$", _("Code devise ISO (ex.: DZD, EUR, USD)."))],
        db_index=True,
        blank=True, null=True
    )

    made_in = models.CharField(_("Nom de la marchandise"), max_length=255, blank=True, null=True)

    # Valeur unitaire saisie (dans `currency`) et en DZD (stockage)
    unit_value_declared = models.DecimalField(max_digits=16, decimal_places=3, validators=[MinValueValidator(Decimal("0"))])
    unit_value_dzd      = models.DecimalField(max_digits=16, decimal_places=3, validators=[MinValueValidator(Decimal("0"))])

    json_initial = models.JSONField(
        null=True, blank=True,
        help_text="Initial goods snapshot payload (single item)."
    )
    json_after = models.JSONField(
        null=True, blank=True,
        help_text="Post-processed/returned payload for this item."
    )

    # Traces (facilite l’audit; nullable pour migration sans prompt)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ["-created_at", "id"]
        indexes = [
            models.Index(fields=["declaration", "name"], name="idx_goods_decl_name"),
            models.Index(fields=["currency"], name="idx_goods_currency"),
        ]
        constraints = [
            models.CheckConstraint(
                name="ck_goods_nonnegative_values",
                check=Q(unit_value_declared__gte=0) & Q(unit_value_dzd__gte=0),
            ),
        ]

    def __str__(self):
        return f"{self.name} × {self.quantity} {self.unit} ({self.currency})"

    # ---------- helpers ----------
    def set_fx_rate(self, rate: Union[Decimal, float, str]):
        """Optionnel: injectez un taux FX (ex. via service) avant save()."""
        self._fx_rate = Decimal(str(rate))

    @property
    def total_value_dzd(self) -> Decimal:
        """Total ligne en DZD."""
        return (self.unit_value_dzd or Decimal("0")) * Decimal(self.quantity or 0)

    # ---------- validation & save ----------
    def clean(self):
        # Normaliser la devise
        if self.currency:
            self.currency = self.currency.strip().upper()
        # Cohérence simple
        if self.quantity is not None and self.quantity <= 0:
            raise ValidationError(_("La quantité doit être > 0."))
        if self.unit_value_declared is None:
            raise ValidationError(_("La valeur unitaire déclarée est requise."))

    def _compute_unit_value_dzd_if_needed(self):
        """
        Règle:
        - Si currency == DZD -> copier la valeur déclarée.
        - Sinon -> si un taux a été injecté via set_fx_rate() on convertit,
          sinon, on laisse la valeur existante (ne pas écraser silencieusement).
        """
        if self.currency == "DZD":
            self.unit_value_dzd = (Decimal(self.unit_value_declared) or Decimal("0")).quantize(
                Decimal("0.001"), rounding=ROUND_HALF_UP
            )
        else:
            rate = getattr(self, "_fx_rate", None)
            if rate is not None:
                self.unit_value_dzd = (Decimal(self.unit_value_declared) * Decimal(rate)).quantize(
                    Decimal("0.001"), rounding=ROUND_HALF_UP
                )
            # sinon: ne pas toucher unit_value_dzd (laisser ce qui a été fourni / calculé ailleurs)
    
    @staticmethod
    def generate_code(length=8):
        """Generate a random string of uppercase letters and digits, excluding 'I', 'l', 'O', 'o', '0'."""
        chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ123456789'
        return ''.join(random.choice(chars) for _ in range(length))
    
    def save(self, *args, **kwargs):
        if self.code == '':
            self.code = self.generate_code()
        self.full_clean()
        # Calcul avant save pour garantir la cohérence
        self._compute_unit_value_dzd_if_needed()
        return super().save(*args, **kwargs)

