from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import hashlib

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


