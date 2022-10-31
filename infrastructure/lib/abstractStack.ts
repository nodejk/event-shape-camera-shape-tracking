import {Construct, Stack, StackProps} from '@aws-cdk/core';

interface AbstractStackProps extends Omit<StackProps, 'env'> {
    
}

abstract class AbstractStack extends Stack {

    protected constructor(scope: Construct, id: string, props: AbstractStackProps) {
        super(scope, id, props ?? {});
    }
}

export {
    AbstractStack,
}