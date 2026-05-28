export interface ApplicationResult {
    prediction: String,
    explanations: Record<string, number>;
}