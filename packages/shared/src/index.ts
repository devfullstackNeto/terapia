export type Role='young_user'|'psychologist'|'admin'|'researcher_aggregated';
export type ChatResponse={text:string;source_refs:{id:string;title:string;source?:string}[];policy_events:string[];response_type:'grounded'|'out_of_scope'|'clinical_refusal'|'safety_escalation'|'dependency_redirect'|'safety_refusal'};
export type MoodCheckin={id:number;mood:1|2|3|4|5;context?:string;created_at:string};
