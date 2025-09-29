// HERE BE GRAPHQL MODEL BE IMPLEMENTED.
// This is coming from back-end api response for the
// GraphQL endpoint. Check app/api/schemas.py

export interface StackItem {
    language: string;
    size: number;
}
export interface UserDataResponse {
    id: string;
    username: string;
    avatarUrl: string;
    stack: StackItem[];
}
