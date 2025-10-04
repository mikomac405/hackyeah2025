export interface PensionInputData {
  age: number;
  gender: 'male' | 'female';
  grossSalary: number;
  workStartYear: number;
  workEndYear?: number;
  currentFunds?: number;
  currentSubFunds?: number;
  sickLeaveImpact?: boolean;
  expectedPension?: number;
  postalCode?: string;
}

export interface PensionCalculationResult {
  realAmount: number;
  inflationAdjustedAmount: number;
  replacementRate: number;
  averagePensionComparison: number;
  sickLeaveImpact?: {
    withSickLeave: number;
    withoutSickLeave: number;
    difference: number;
    percentageImpact: number;
  };
  delayedRetirementScenarios: {
    oneYear: { amount: number; increase: number };
    twoYears: { amount: number; increase: number };
    fiveYears: { amount: number; increase: number };
  };
  requiredWorkExtension?: number;
  fundsGrowthTimeline: Array<{
    year: number;
    age: number;
    totalFunds: number;
    annualContribution: number;
  }>;
}

export interface PensionGroup {
  name: string;
  description: string;
  averageAmount: number;
  percentage: number;
  color: string;
  detailedInfo: string;
}

export interface UsageLogData {
  timestamp: Date;
  expectedPension?: number;
  age: number;
  gender: 'male' | 'female';
  grossSalary: number;
  sickLeaveIncluded: boolean;
  currentFunds?: number;
  realPension: number;
  inflationAdjustedPension: number;
  postalCode?: string;
}

export interface RegionalStats {
  region: string;
  averagePension: number;
  participantsCount: number;
  medianAge: number;
}

export interface HistoricalData {
  averageSalaries: number[];
  inflationRates: number[];
  pensionFundGrowth: number[];
  years: number[];
}