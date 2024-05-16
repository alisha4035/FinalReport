from aws_cdk import (
    aws_codebuild as codebuild,
    aws_codecommit as codecommit,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cpactions,
    aws_s3 as s3,
    aws_iam as iam,
    CfnOutput,
    Stack,
)
from constructs import Construct


class SwPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Creates an AWS CodeCommit repository
        code_repo = codecommit.Repository(
            self, "SWPipelineRepo",
            repository_name="SWPipelineRepo",
            code=codecommit.Code.from_zip_file("sw_pipeline/Java-Project.zip")
        )
        
        #Creates an S3 artifact bucket
        code_bucket = s3.Bucket(self, "SWPipelineBucket")
        
        #Creating my CodeBuild project
        code_build = codebuild.Project(self, "SWPipelineBuild",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2"
            }),
            source=codebuild.Source.code_commit(repository=code_repo),
            artifacts=codebuild.Artifacts.s3(bucket=code_bucket)
        )
        
        #Creating my IAM role
        code_iam_role = iam.Role(self, "AppBuildRole",
            assumed_by=iam.ServicePrincipal("codepipeline.amazonaws.com"),
            path="/service-role/"
        )
        
        code_iam_role.add_to_policy(
            iam.PolicyStatement(
            actions=[
                "s3:PutObject",
                "s3:GetObject",
                "s3:GetBucketAcl",
                "s3:GetBucketLocation"
            ],
            effect=iam.Effect.ALLOW,
            resources=[code_bucket.bucket_arn]
            )
        )
        
        code_iam_role.add_to_policy(
            iam.PolicyStatement(
            actions=[
                "codecommit:CancelUploadArchive",
                "codecommit:GetBranch",
                "codecommit:GetCommit",
                "codecommit:GetUploadArchiveStatus",
                "codecommit:UploadArchive"
            ],
            effect=iam.Effect.ALLOW,
            resources=[code_repo.repository_arn]
            )
        )
        
        code_iam_role.add_to_policy(
            iam.PolicyStatement(
            actions=[
                "codebuild:BatchGetBuilds",
                "codebuild:StartBuild"
            ],
            effect=iam.Effect.ALLOW,
            resources=[code_build.project_arn]
            )
        )
        
        code_pipeline = codepipeline.Pipeline(self, "SWPipeline",
            artifact_bucket=code_bucket,
            role=code_iam_role)
            
        source_output = codepipeline.Artifact("SourceArtifact")
        source_action = cpactions.CodeCommitSourceAction(
            action_name="Source",
            repository=code_repo,
            output=source_output
        )
        
        build_output = codepipeline.Artifact()
        build_action = cpactions.CodeBuildAction(
            action_name="Build",
            project=code_build,
            input=source_output,
            outputs=[build_output]
        )
        
        
        code_pipeline.add_stage(
            stage_name="Source",
            actions=[source_action]
        )
        
        code_pipeline.add_stage(
            stage_name="Build",
            actions=[build_action]
        )

