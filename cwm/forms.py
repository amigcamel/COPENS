#-*-coding:utf-8-*-
from django import forms
from django.forms.extras.widgets import SelectDateWidget

CHOICE = (
    (u'新聞', (('cna', '中央通訊社'),('asbc', '中研院平衡語料庫'))),
    (u'社會網絡', (('plurk', u'噗浪'), ('ptt', u'批踢踢'))),
    (u'政治法律', (('president', u'總統文告'), ('sunflower', u'太陽花學運'), ('ly', u'立法院公報'))),
    (u'兒童習得', (('tccm', '台灣兒童語言語料庫'), ('textbook', u'國小教科書'))),
    (u'口語言談', (('ntuspk', '台大口語語料庫'),)),
    (u'成語語料', (('chinatext', '網路新聞語料'),)),
#    (u'世界中文', (('china', u'中國'), ('hongkong', u'香港'), ('singapore', u'新加坡'))),
    (u'其他', (('copener', 'COPEN user'),)),
)

DB_CHOICE = []
for cat, corps in CHOICE:
    for corp in corps:
        DB_CHOICE.append(corp)


dbdic = dict(DB_CHOICE)

class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'required':'required', 'placeholder':u"請輸入關鍵字",'id':'namanyay-search-box', 'size':40}), min_length=1, max_length=300, error_messages={'required':'請輸入關鍵字'})
    database = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=DB_CHOICE, error_messages={'required':'請至少選擇一項'})

class ColloForm(forms.Form):
    algorithms = forms.ChoiceField(choices=[('chi_sq', 'chi_sq'),
                                            ('likelihood_ratio', 'likelihood_ratio'),
                                            ('pmi', 'pmi'),
                                            ('student_t', 'student_t'),
                                            ('dice', 'dice'),
                                            ('mi_like', 'mi_like'),
                                            ('poisson_stirling', 'poisson_stirling'),
                                            ('jaccard', 'jaccard'),
                                            ('phi_sq', 'phi_sq'),
                                            ('raw_freq', 'raw_freq')], label="演算法", help_text="選擇欲使用之演算法") 
    stopword_filter = forms.IntegerField(min_value=1, 
                                         max_value=500, 
                                         required=False, 
                                         widget=forms.NumberInput(attrs={'placeholder':'none'}),
                                         label="停用詞篩選數量",
                                         help_text="使用停用詞篩選可以過濾一些高頻詞如「的」、「我」等僅具有句法功能之字詞")
     
class ConcForm(forms.Form):
    pos = forms.BooleanField(required=False, label=("顯示詞類"), help_text="在結果中顯示詞性，若取消勾選，搜尋速度較快")
    window_size = forms.IntegerField(min_value=1, max_value=10, initial=8, widget=forms.NumberInput(attrs={'onkeydown':"return false"}), label="詞語索引左右顯示數量", help_text="關鍵字之左/右顯示之字數")
    sampling = forms.BooleanField(required=False, label=('隨機抽樣'), help_text="針對所有結果進行隨機抽樣,點選進行抽樣數目調整")
    sampling_num = forms.IntegerField(min_value=1, initial=1, label=("隨機抽樣數目"))
    display_num = forms.IntegerField(initial=100, min_value=100, max_value=1000, widget=forms.NumberInput(attrs={'step':'100', 'onkeydown':"return false"}), label=("每頁顯示筆數"), help_text="每頁顯示詞語索引數量")

class SketchForm(forms.Form):
    min_logdice = forms.FloatField(required=False, label=("Minimal logdice value"), widget=forms.NumberInput(attrs={'placeholder':'可為空白'})) 
    min_occ = forms.IntegerField(required=False, label=("Minimal occurrence"), widget=forms.NumberInput(attrs={'placeholder':'可為空白'}))

class KeynessForm(forms.Form):
    reference_corpus = forms.ChoiceField(choices=DB_CHOICE)


from registration.forms import RegistrationFormTermsOfService
from captcha.fields import CaptchaField

from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationForm


from django.contrib.auth.models import User
import re
def ajiEmailValidator(email):
    allow_list = ['@gmail\.', '@hotmail\.', '@yahoo\.', '@.*?\.edu']
    pat = re.compile('|'.join(allow_list))
    if not pat.search(email):
        raise forms.ValidationError(u'Sorry, you can\'t use this email!')
    if User.objects.filter(email=email).exists():
        raise forms.ValidationError(u'This email has been used!')

class LopeRegForm(RegistrationForm):
    # modify from here: /usr/local/lib/python2.7/dist-packages/registration/forms.py
    username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                max_length=30,
                                label=("Username"),
                                widget=forms.TextInput(attrs={'placeholder': 'Username', 'required':'required'}),
                                error_messages={'invalid': ("This value may contain only letters, numbers and @/./+/-/_ characters.")})

    email = forms.EmailField(validators=[ajiEmailValidator], label=("E-mail"), widget=forms.EmailInput(attrs={'placeholder': 'Email', 'required':'required'}), help_text="僅可使用gmail, hotmail, yahoo 或.edu 網域 (例：foo@ntu.edu.tw) 申請註冊")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 'required':'required'}),
                                label=("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password (again)', 'required':'required'}),
                                label=("Password (again)"))

    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs={'required':'required'}),
                             label=(u'I have read and agree to the Terms of Service'),
                             error_messages={'required': ("You must agree to the terms to register")})
    captcha = CaptchaField()  
    
