from django.contrib.auth.models import User
from api.models import Projects, Issues, Contributors, Comments
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'type', 'author_user_id', 'description', ]


class ProjectDetailSerializer(ModelSerializer):
    class Meta:
        model = Projects
        fields = ['id', 'title', 'description', 'type', 'author_user_id', ]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'issue_id', 'description', 'author_user_id', 'created_time']


class CommentAddSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ['id', 'description', 'author_user_id']


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = ['id', 'title', 'desc', 'tag', 'priority', 'project_id',
                  'status', 'author_user_id', 'assignee_user_id', 'created_time']


class IssueAddForProjectSerializer(ModelSerializer):
    class Meta:
        model = Issues
        fields = ['id', 'title', 'desc', 'tag', 'priority',
                  'status', 'author_user_id', 'assignee_user_id', 'created_time']


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['id', 'user_id', 'project_id', 'permission', 'role']


class ContributorDetailsSerializer(ModelSerializer):
    class Meta:
        model = Contributors
        fields = ['id', 'user_id', 'project_id', 'permission', 'role']
