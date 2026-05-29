export interface ApplicationResult {
    prediction: number,
    decision: string,
    explanations: Record<string, number>;
}