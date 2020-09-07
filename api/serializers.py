from accounts.models import UserProfile, ProgrammingLanguage
from questions.models import Question
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserProfile
		fields = "__all__"

class ProgrammingLanguageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProgrammingLanguage
		fields = "__all__"

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		fields = "__all__"

class PrettyJSONRender(JSONRenderer):
	def get_indent(self, *args, **kwargs):
		return 2