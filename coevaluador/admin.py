from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Course)
admin.site.register(Coevaluation)
admin.site.register(Question)
admin.site.register(CoevaluationSheet)
admin.site.register(Answer)
admin.site.register(WorkTeam)
admin.site.register(TeamMember)
