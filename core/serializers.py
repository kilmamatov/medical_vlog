from rest_framework import serializers

from core.models import CommentModel, PostModel, TagModel


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagModel
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ["text"]


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = PostModel
        fields = ["tags", "title", "text", "photo"]

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        post = PostModel.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, created = TagModel.objects.get_or_create(**tag_data)
            post.tags.add(tag)

        return post
