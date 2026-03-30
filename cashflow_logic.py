import pandas as pd

class IndirectCashFlowEngine:
    """
    Standardized Cash Flow Engine (Indirect Method) 
    Compliant with IFRS (IAS 7) and ACCA Reporting Standards.
    Architected by: Vishwa Y Bhatt
    """

    def __init__(self, net_income, depreciation, tax_paid, interest_paid):
        self.net_income = net_income
        self.depreciation = depreciation # Non-cash add-back
        self.tax_paid = tax_paid         # Disclosed separately under IAS 7
        self.interest_paid = interest_paid
        self.working_capital_changes = []

    def add_wc_change(self, account_name, opening_bal, closing_bal, is_asset=True):
        """
        Calculates the cash impact of Working Capital changes.
        Assets: Increase = Outflow (-) | Decrease = Inflow (+)
        Liabilities: Increase = Inflow (+) | Decrease = Outflow (-)
        """
        change = closing_bal - opening_bal
        impact = -change if is_asset else change
        self.working_capital_changes.append({"Account": account_name, "Impact": impact})

    def generate_statement(self):
        print(f"{'='*50}")
        print(f"{'CASH FLOW STATEMENT (INDIRECT METHOD)':^50}")
        print(f"{'In accordance with IAS 7 / IFRS':^50}")
        print(f"{'='*50}\n")

        # 1. Operating Activities
        print(f"1. CASH FLOWS FROM OPERATING ACTIVITIES")
        print(f"Profit Before Tax (PBT):".ljust(35), f"£{self.net_income:,.0f}")
        print(f"Adjustments for non-cash items:")
        print(f"  + Depreciation & Amortization:".ljust(35), f"£{self.depreciation:,.0f}")
        
        # 2. Working Capital Changes
        wc_total = 0
        print(f"Changes in Working Capital:")
        for item in self.working_capital_changes:
            prefix = "(Increase)" if item['Impact'] < 0 else "Decrease"
            label = f"  {prefix} in {item['Account']}:"
            print(label.ljust(35), f"£{item['Impact']:,.0f}")
            wc_total += item['Impact']

        # 3. Final Operating Totals
        cash_from_ops = self.net_income + self.depreciation + wc_total
        print(f"{'-'*50}")
        print(f"Cash Generated from Operations:".ljust(35), f"£{cash_from_ops:,.0f}")
        print(f"  - Interest Paid:".ljust(35), f"£({self.interest_paid:,.0f})")
        print(f"  - Income Tax Paid:".ljust(35), f"£({self.tax_paid:,.0f})")
        
        net_operating_cash = cash_from_ops - self.interest_paid - self.tax_paid
        print(f"{'='*50}")
        print(f"NET CASH FROM OPERATING ACTIVITIES:".ljust(35), f"£{net_operating_cash:,.0f}")

# --- EXECUTION FOR PORTFOLIO DEMO ---
if __name__ == "__main__":
    # Sample SME / Agency Data
    engine = IndirectCashFlowEngine(
        net_income=250000, 
        depreciation=15000, 
        tax_paid=45000, 
        interest_paid=8000
    )

    # Adding Working Capital Movements (Opening vs Closing)
    engine.add_wc_change("Trade Receivables", 120000, 155000, is_asset=True)  # Outflow
    engine.add_wc_change("Inventory", 40000, 35000, is_asset=True)            # Inflow
    engine.add_wc_change("Trade Payables", 80000, 95000, is_asset=False)      # Inflow

    engine.generate_statement()
