import datetime
import pandas as pd
import numpy as np

class CashFlow(object):

    def __init__(self, person, periods=30*12, start_date=None):
        """
        Args:
            person
            periods
            start_date

        """
        self.person = person
        self.periods = periods
        self.start_date = start_date

        salary = person.salary
        salary_growth_rate = person.salary_growth_rate
        current_expenses = person.current_expenses
        expenses = person.expenses

        if start_date is None:
            today = datetime.datetime.today()
            if today.month == 12:
                start_date = datetime.datetime(today.year + 1, 1, 1)
            else:
                start_date = datetime.datetime(today.year, today.month + 1, 1)

        index = pd.period_range(start=start_date, periods=periods, freq='M')

        columns = ['income']

        ts = pd.DataFrame(None, index=index, columns=columns, dtype=pd.np.float)

        # Set salary
        salary_growth_factor_monthly = (1 + salary_growth_rate)**(1./12.)
        monthly_salary = salary / 12.
        ts.loc[:, 'income'] = (np.ones(len(index)) * salary_growth_factor_monthly).cumprod() * monthly_salary

        # Set expenses for each category
        for i in expenses:
            ts[i.name] = np.ones(len(index)) * i.amount / 12.

        # Set total expense
        monthly_expense = current_expenses / 12.
        ts['total expense'] = np.ones(len(index)) * monthly_expense

        # Set net income
        ts['net income'] = ts.loc[:, 'income'] - ts.loc[:, 'total expense']
        self.ts = ts

    @staticmethod
    def _ts_to_dict(ts):
        from numpy import isnan
        return {
            k: [
                v if isinstance(v, str) or (v is not None and not isnan(v)) else None
                for v in values
            ]
            for k, values in ts.to_dict(orient='series').items()
        }

    def to_dict(self):
        return {
            'person': self.person.to_dict(),
            'periods': self.periods,
            'start_date': self.start_date,
            'ts': self._ts_to_dict(self.ts)
        }

    def run(self):
        ts = self.ts
        return ts
