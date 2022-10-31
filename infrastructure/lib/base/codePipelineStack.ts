import { Stack } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as codecommit from 'aws-cdk-lib/aws-codecommit';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import {Artifact, Pipeline} from 'aws-cdk-lib/aws-codepipeline';
import * as codepipeline_actions from 'aws-cdk-lib/aws-codepipeline-actions';
import {CodeStarConnectionsSourceAction, S3SourceAction} from 'aws-cdk-lib/aws-codepipeline-actions';
import {AbstractStack} from '../abstractStack';

export type CodePipelineConstructPropsBase = {
    readonly projectName: string;
} & CodePipelineConstructPropsGithubSource;

export type CodePipelineConstructProps = {
    readonly dataManifestBucket: s3.Bucket;
    readonly sageMakerArtifactBucket: s3.Bucket;
    readonly sageMakerExecutionRole: iam.Role;
} & CodePipelineConstructPropsBase;

export interface CodePipelineConstructPropsGithubSource {
    readonly repoType: 'git';
    readonly git: {
        readonly githubConnectionArn: string;
        readonly githubRepoOwner: string;
        readonly githubRepoName: string;
        readonly githubRepoBranch?: string;
    };
}

export interface CodePipelineConstructPropsCodeCommitSource {
    readonly repoType: 'codecommit';
}

export class CodePipelineConstruct extends AbstractStack {
    readonly pipeline: Pipeline;
    readonly projectName: string;
    readonly bucketArn: string;

    constructor (scope: Construct, id: string, props: CodePipelineConstructProps) {
        super(scope, id, props);

        this.pipeline = new Pipeline(this, 'EventCameraPipeline', {
            restartExecutionOnUpdate: true,
        });

        this.projectName = props.projectName;
        this.bucketArn = props.dataManifestBucket.bucketArn;

        const sourceCodeOutput = new Artifact('EventCameraCodeOutput');
        const sourceDataOutput = new Artifact('EventCameraDataOutput');
        const buildOutput = new Artifact('BuildOutput');
        const pipelineOutput = new Artifact('PipelineOutput');

        const sourceCode = new CodeStarConnectionsSourceAction({
            actionName: 'SourceCode',
            output: sourceCodeOutput,
            owner: props.git.githubRepoOwner,
            repo: props.git.githubRepoName,
            branch: props.git.githubRepoBranch || 'main',
            connectionArn: props.git.githubConnectionArn,
        });

        const sourceData = new S3SourceAction({
            actionName: 'SourceData',
            output: sourceDataOutput,
            bucket: props.dataManifestBucket,
            bucketKey: 'manifest.json.zip'
        });

        this.pipeline.addStage({
            stageName: 'Source',
            actions: [sourceCode, sourceData],
        });

        
    }

    private mlPipelineRole(): iam.Role {
        const mlPipelineRole = new iam.Role(this, 'MLPipelineRole', {
            assumedBy: new iam.ServicePrincipal('codebuild.amazonaws.com'),
        });

        mlPipelineRole.addToPolicy(
            iam.PolicyStatement.fromJson({
                Effect: 'Allow',
                Action: ['s3:CreateBucket', 's3:GetObject', 's3:PutObject', 's3:ListBucket'],
                Resource: [this.bucketArn, `${this.bucketArn}/*`],
            })
        );

        mlPipelineRole.addToPolicy(
            iam.PolicyStatement.fromJson({
                Effect: 'Allow',
                Action: [
                    'sagemaker:CreatePipeline',
                    'sagemaker:ListTags',
                    'sagemaker:AddTags',
                    'sagemaker:UpdatePipeline',
                    'sagemaker:DescribePipeline',
                    'sagemaker:StartPipelineExecution',
                    'sagemaker:DescribePipelineExecution',
                    'sagemaker:ListPipelineExecutionSteps',
                ],
                Resource: [
                    `arn:aws:sagemaker:${Stack.of(this).region}:${Stack.of(this).account}:pipeline/${
                        this.projectName
                    }`,
                    `arn:aws:sagemaker:${Stack.of(this).region}:${Stack.of(this).account}:pipeline/${
                        this.projectName
                    }/*`,
                ],
            })
        );

        return mlPipelineRole;
    }
}