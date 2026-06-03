export interface ApplicationResult {
    prediction: number,
    decision: string,
    userAdvice: {
        GOOD: [number, string][],
        BAD: [number, string][],
        INFO: [number, string][]
    },
    explanations: Record<string, number>;
}