# Join results
echo "Joining sensitivity analysis results"
bart join 10 irbssfp/sens_{R1,R2,B1} testing/sens

echo "Joining partial gradient derivatives results"
bart join 10 irbssfp/grad_{R1,R2,B1} testing/grad

# Get NMRSE between replication results and reference
nrmse_sens=$(bart nrmse testing/sens ref/sens) # for sensitivity analysis
echo "NMRSE for sensitivity analysis results is ${nrmse_sens}"

nrmse_grad=$(bart nrmse testing/grad ref/grad) # for partial gradient derivatives
echo "NMRSE for partial gradient derivatives results is ${nrmse_grad}"
