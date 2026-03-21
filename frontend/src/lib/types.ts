import { z } from 'zod';

// --- SSE event name union (frozen per constitution Principle III) ---
export type SSEEventName =
  | 'marketplace_products'
  | 'viability_score'
  | 'target_persona'
  | 'differentiation_angles'
  | 'competitive_overview'
  | 'export_ready'
  | 'source_unavailable';

// --- Connection state ---
export type ConnectionState = 'idle' | 'connecting' | 'streaming' | 'complete' | 'error';

// --- Section display state ---
export type SectionState = 'hidden' | 'loading' | 'streaming' | 'complete' | 'error';

// --- Marketplace products ---
export const MarketplaceProductSchema = z.object({
  title: z.string(),
  price: z.string(),
  url: z.string(),
});

export const MarketplaceProductsEventSchema = z.object({
  status: z.literal('complete'),
  products: z.array(MarketplaceProductSchema),
});

export type MarketplaceProduct = z.infer<typeof MarketplaceProductSchema>;
export type MarketplaceProductsEvent = z.infer<typeof MarketplaceProductsEventSchema>;

// --- LLM section events (streaming / complete / error) ---
export const LLMTokenEventSchema = z.object({
  status: z.literal('streaming'),
  token: z.string(),
});

export const LLMCompleteEventSchema = z.object({
  status: z.literal('complete'),
  content: z.string(),
  score: z.number().int().min(0).max(100).nullable().optional(),
});

export const LLMErrorEventSchema = z.object({
  status: z.literal('error'),
  partial_content: z.string().optional().default(''),
  message: z.string(),
});

export const LLMSectionEventSchema = z.union([
  LLMTokenEventSchema,
  LLMCompleteEventSchema,
  LLMErrorEventSchema,
]);

export type LLMTokenEvent = z.infer<typeof LLMTokenEventSchema>;
export type LLMCompleteEvent = z.infer<typeof LLMCompleteEventSchema>;
export type LLMErrorEvent = z.infer<typeof LLMErrorEventSchema>;
export type LLMSectionEvent = z.infer<typeof LLMSectionEventSchema>;

// --- Source unavailable ---
export const SourceUnavailableEventSchema = z.object({
  source: z.enum(['amazon', 'google_trends', 'reddit']),
  message: z.string(),
});

export type SourceUnavailableEvent = z.infer<typeof SourceUnavailableEventSchema>;

// --- Export ready ---
export const ExportReadyEventSchema = z.object({
  status: z.literal('complete'),
});

export type ExportReadyEvent = z.infer<typeof ExportReadyEventSchema>;
