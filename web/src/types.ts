export type Parallel = {
  uid?: string | null;
  acronym?: string | null;
  root_lang?: string | null;
  original_title?: string | null;
  translated_title?: string | null;
  type?: string | null;
  resembling?: boolean | null;
  remark?: string | null;
};

export type SutraRecord = {
  id: string;
  uid: string;
  title: string;
  chinese_text: string;
  english_sa_text: string;
  parallels: Parallel[];
  primary_sn_uid?: string | null;
  pali_text: string;
  english_sn_text: string;
  kumarajiva_style_text: string;
  modern_psychology_text: string;
  notes?: string;
  review_status?: string;
  translator?: string;
  confidence?: string;
  errors?: string[];
  forbidden_hits?: string[];
  validation?: {
    status?: string;
    issues?: string[];
    warnings?: string[];
    forbidden_hits?: string[];
  };
};
