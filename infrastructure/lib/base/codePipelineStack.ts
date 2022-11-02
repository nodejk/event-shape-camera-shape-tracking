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
}