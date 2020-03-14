from django.forms import ModelForm

from webapp.models import ScholarshipApplication


class ScholarshipApplicationForm(ModelForm):
    class Meta:
        model = ScholarshipApplication
        fields = [
            'student_name',
            'address',
            'email',
            'phone_number',
            'birth_certificate',
            'id_no',
            'school_name',
            'school_address',
            'academic_level',
            'recommendation_reason',
            'recommendation_letter'

        ]


