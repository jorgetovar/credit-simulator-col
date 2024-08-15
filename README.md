# Credit Simulator Colombia 🇨🇴

## Overview

This Credit Simulator helps you make informed decisions about housing loans in Colombian Pesos (COP). It demonstrates how Python can transform a daunting debt into a manageable one through smart financial planning.

## Why This Matters

Purchasing a home is a significant decision, and the associated credits can be overwhelming. This repository allows you to compare various scenarios and make the best decision for your financial situation.

Key takeaways:
- Pay more than the minimum: Allocate extra funds towards your debt when possible.
- Consider refinancing: It can significantly reduce your overall interest payments.

> Remember: Information is power! 🔥

## Scenarios

### Scenario 1: Minimum Payments

```shell
************************* 
------ Overview ------ 
Total paid interest: $174,443,906.52 
Total paid fee insurances: $28,429,449.01 
Monthly principal: $0.00 
Total paid: $502,873,355.54 
Total principal: $0.00 
...
Total years reduced: 0.0 
************************* 
```

### Scenario 2: Extra Monthly Payment

```shell
************************* 
------ Overview ------ 
Total paid interest: $118,124,714.83 
Total paid fee insurances: $19,677,591.39 
Monthly principal: $1,000,000.00 
Total paid: $440,742,025.18 
Total principal: $85,000,000.00 
...
Total years reduced: 2.916666666666667 
************************* 
```

### Scenario 3: Larger Extra Monthly Payment

```shell
************************* 
------ Overview ------ 
Total paid interest: $88,098,623.41 
Total paid fee insurances: $15,542,848.06 
Monthly principal: $1,000,000.00 
Total paid: $407,255,492.75 
Total principal: $111,000,000.00 
...
Total years reduced: 4.083333333333333 
************************* 
```

## API Access

This simulator is also available as an API, allowing you to integrate these calculations into your own applications or scripts.

### Example API Call

Use the following curl command to simulate a credit scenario:

```bash
curl --location 'https://credit-simulator-col.fly.dev/credit/simulate?first_due_date=2024-08-25' \
--header 'Content-Type: application/json' \
--data '{
    "property_price": 168000000,
    "total_due": 120000000,
    "interest_rate_per_year": 0.103999,
    "installments": 60,
    "fee_life_insurance": 130000,
    "fee_disaster_insurance": 100000
    "monthly_principal": 100000 # optional
}'
```

This API call simulates a credit scenario with the following parameters:
- Property Price: 168,000,000 COP
- Total Due: 120,000,000 COP
- Annual Interest Rate: 10.3999%
- Installments: 60 months
- Monthly Life Insurance Fee: 130,000 COP
- Monthly Disaster Insurance Fee: 100,000 COP
- Monthly Principal: 100,000 COP (Optional)

Feel free to adjust these parameters to match your specific scenario.

## Conclusion

By leveraging this Credit Simulator, you can make more informed decisions about your housing loan. Remember, small changes in your payment strategy can lead to significant savings over time.

## Contributing

Contributions are welcome! If you have ideas for improvements or new features, please open an issue or submit a pull request.


> Happy simulating, and may your financial decisions be ever in your favor! 💰🏠
