from rest_framework import serializers

from core.models import Tag, Post


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['tags', 'title', 'text', 'photo']

    def create(self, validated_data):
        if validated_data.get('tags'):
            tags_data = validated_data.pop('tags')
            post = Post.objects.create(**validated_data)
            for tag_data in tags_data:
                Tag.objects.create(post=post, **tag_data)
        post = Post.objects.create(**validated_data)
        return post
