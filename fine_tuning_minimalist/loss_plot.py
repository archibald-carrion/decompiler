import matplotlib.pyplot as plt
import ast

# Hardcoded training data
training_data = [
    {'loss': 5.4817, 'grad_norm': 16.00971221923828, 'learning_rate': 0.0, 'epoch': 0.07},
    {'loss': 5.5958, 'grad_norm': 15.76498031616211, 'learning_rate': 5.000000000000001e-07, 'epoch': 0.13},
    {'loss': 5.4757, 'grad_norm': 15.294819831848145, 'learning_rate': 1.0000000000000002e-06, 'epoch': 0.2},
    {'loss': 5.4238, 'grad_norm': 15.323972702026367, 'learning_rate': 1.5e-06, 'epoch': 0.27},
    {'loss': 5.0566, 'grad_norm': 14.739215850830078, 'learning_rate': 2.0000000000000003e-06, 'epoch': 0.33},
    {'loss': 5.7443, 'grad_norm': 13.820405960083008, 'learning_rate': 2.5e-06, 'epoch': 0.4},
    {'loss': 5.4117, 'grad_norm': 13.653189659118652, 'learning_rate': 3e-06, 'epoch': 0.47},
    {'loss': 5.5295, 'grad_norm': 12.97104263305664, 'learning_rate': 3.5000000000000004e-06, 'epoch': 0.53},
    {'loss': 5.1675, 'grad_norm': 12.879201889038086, 'learning_rate': 4.000000000000001e-06, 'epoch': 0.6},
    {'loss': 4.9426, 'grad_norm': 11.767942428588867, 'learning_rate': 4.5e-06, 'epoch': 0.67},
    {'loss': 5.5, 'grad_norm': 12.166486740112305, 'learning_rate': 5e-06, 'epoch': 0.73},
    {'loss': 5.1795, 'grad_norm': 10.560510635375977, 'learning_rate': 5.500000000000001e-06, 'epoch': 0.8},
    {'loss': 5.1207, 'grad_norm': 10.707776069641113, 'learning_rate': 6e-06, 'epoch': 0.87},
    {'loss': 5.0792, 'grad_norm': 10.002942085266113, 'learning_rate': 6.5000000000000004e-06, 'epoch': 0.93},
    {'loss': 4.6105, 'grad_norm': 9.704378128051758, 'learning_rate': 7.000000000000001e-06, 'epoch': 1.0},
    {'loss': 4.6494, 'grad_norm': 9.205781936645508, 'learning_rate': 7.5e-06, 'epoch': 1.07},
    {'loss': 4.4738, 'grad_norm': 8.497492790222168, 'learning_rate': 8.000000000000001e-06, 'epoch': 1.13},
    {'loss': 4.6779, 'grad_norm': 8.550384521484375, 'learning_rate': 8.500000000000002e-06, 'epoch': 1.2},
    {'loss': 4.5084, 'grad_norm': 8.343538284301758, 'learning_rate': 9e-06, 'epoch': 1.27},
    {'loss': 4.5638, 'grad_norm': 8.128386497497559, 'learning_rate': 9.5e-06, 'epoch': 1.33},
    {'loss': 4.6151, 'grad_norm': 8.265108108520508, 'learning_rate': 1e-05, 'epoch': 1.4},
    {'loss': 4.1545, 'grad_norm': 8.074475288391113, 'learning_rate': 1.05e-05, 'epoch': 1.47},
    {'loss': 4.2446, 'grad_norm': 8.814181327819824, 'learning_rate': 1.1000000000000001e-05, 'epoch': 1.53},
    {'loss': 3.9292, 'grad_norm': 9.811898231506348, 'learning_rate': 1.1500000000000002e-05, 'epoch': 1.6},
    {'loss': 3.8051, 'grad_norm': 9.878616333007812, 'learning_rate': 1.2e-05, 'epoch': 1.67},
    {'loss': 4.2945, 'grad_norm': 9.707437515258789, 'learning_rate': 1.25e-05, 'epoch': 1.73},
    {'loss': 4.0951, 'grad_norm': 10.227054595947266, 'learning_rate': 1.3000000000000001e-05, 'epoch': 1.8},
    {'loss': 4.1282, 'grad_norm': 10.17094612121582, 'learning_rate': 1.3500000000000001e-05, 'epoch': 1.87},
    {'loss': 3.7716, 'grad_norm': 11.696235656738281, 'learning_rate': 1.4000000000000001e-05, 'epoch': 1.93},
    {'loss': 3.7701, 'grad_norm': 12.237848281860352, 'learning_rate': 1.45e-05, 'epoch': 2.0},
    {'loss': 3.397, 'grad_norm': 13.344131469726562, 'learning_rate': 1.5e-05, 'epoch': 2.07},
    {'loss': 3.502, 'grad_norm': 13.840869903564453, 'learning_rate': 1.55e-05, 'epoch': 2.13},
    {'loss': 3.433, 'grad_norm': 14.31462574005127, 'learning_rate': 1.6000000000000003e-05, 'epoch': 2.2},
    {'loss': 3.3398, 'grad_norm': 16.6142635345459, 'learning_rate': 1.65e-05, 'epoch': 2.27},
    {'loss': 3.5622, 'grad_norm': 15.18295955657959, 'learning_rate': 1.7000000000000003e-05, 'epoch': 2.33},
    {'loss': 3.4533, 'grad_norm': 18.162376403808594, 'learning_rate': 1.75e-05, 'epoch': 2.4},
    {'loss': 3.4501, 'grad_norm': 18.38132095336914, 'learning_rate': 1.8e-05, 'epoch': 2.47},
    {'loss': 3.395, 'grad_norm': 18.934873580932617, 'learning_rate': 1.85e-05, 'epoch': 2.53},
    {'loss': 3.1046, 'grad_norm': 20.9205379486084, 'learning_rate': 1.9e-05, 'epoch': 2.6},
    {'loss': 3.3539, 'grad_norm': 21.940380096435547, 'learning_rate': 1.9500000000000003e-05, 'epoch': 2.67},
    {'loss': 3.4209, 'grad_norm': 20.977046966552734, 'learning_rate': 2e-05, 'epoch': 2.73},
    {'loss': 2.969, 'grad_norm': 23.392385482788086, 'learning_rate': 2.05e-05, 'epoch': 2.8},
    {'loss': 3.3312, 'grad_norm': 23.759416580200195, 'learning_rate': 2.1e-05, 'epoch': 2.87},
    {'loss': 2.883, 'grad_norm': 24.00092887878418, 'learning_rate': 2.15e-05, 'epoch': 2.93},
    {'loss': 3.1757, 'grad_norm': 21.833641052246094, 'learning_rate': 2.2000000000000003e-05, 'epoch': 3.0},
    {'loss': 2.8909, 'grad_norm': 23.638566970825195, 'learning_rate': 2.25e-05, 'epoch': 3.07},
    {'loss': 2.7662, 'grad_norm': 23.392934799194336, 'learning_rate': 2.3000000000000003e-05, 'epoch': 3.13},
    {'loss': 2.8586, 'grad_norm': 22.033275604248047, 'learning_rate': 2.35e-05, 'epoch': 3.2},
    {'loss': 3.0399, 'grad_norm': 22.656633377075195, 'learning_rate': 2.4e-05, 'epoch': 3.27},
    {'loss': 2.6773, 'grad_norm': 24.993240356445312, 'learning_rate': 2.45e-05, 'epoch': 3.33},
    {'loss': 2.5081, 'grad_norm': 24.885644912719727, 'learning_rate': 2.5e-05, 'epoch': 3.4},
    {'loss': 2.879, 'grad_norm': 23.356197357177734, 'learning_rate': 2.5500000000000003e-05, 'epoch': 3.47},
    {'loss': 2.7958, 'grad_norm': 25.17336654663086, 'learning_rate': 2.6000000000000002e-05, 'epoch': 3.53},
    {'loss': 2.8752, 'grad_norm': 25.02996063232422, 'learning_rate': 2.6500000000000004e-05, 'epoch': 3.6},
    {'loss': 2.4947, 'grad_norm': 27.29197883605957, 'learning_rate': 2.7000000000000002e-05, 'epoch': 3.67},
    {'loss': 2.9688, 'grad_norm': 23.9234561920166, 'learning_rate': 2.7500000000000004e-05, 'epoch': 3.73},
    {'loss': 2.6077, 'grad_norm': 25.89621925354004, 'learning_rate': 2.8000000000000003e-05, 'epoch': 3.8},
    {'loss': 2.5078, 'grad_norm': 28.974809646606445, 'learning_rate': 2.8499999999999998e-05, 'epoch': 3.87},
    {'loss': 2.6932, 'grad_norm': 27.146432876586914, 'learning_rate': 2.9e-05, 'epoch': 3.93},
    {'loss': 2.7187, 'grad_norm': 25.871601104736328, 'learning_rate': 2.95e-05, 'epoch': 4.0},
    {'loss': 2.6038, 'grad_norm': 26.80230140686035, 'learning_rate': 3e-05, 'epoch': 4.07},
    {'loss': 2.3838, 'grad_norm': 28.022754669189453, 'learning_rate': 3.05e-05, 'epoch': 4.13},
    {'loss': 2.4991, 'grad_norm': 27.59710121154785, 'learning_rate': 3.1e-05, 'epoch': 4.2},
    {'loss': 2.2479, 'grad_norm': 29.955385208129883, 'learning_rate': 3.15e-05, 'epoch': 4.27},
    {'loss': 2.4369, 'grad_norm': 28.899721145629883, 'learning_rate': 3.2000000000000005e-05, 'epoch': 4.33},
    {'loss': 2.4234, 'grad_norm': 29.87893295288086, 'learning_rate': 3.2500000000000004e-05, 'epoch': 4.4},
    {'loss': 2.2556, 'grad_norm': 29.47521209716797, 'learning_rate': 3.3e-05, 'epoch': 4.47},
    {'loss': 2.1345, 'grad_norm': 30.75361442565918, 'learning_rate': 3.35e-05, 'epoch': 4.53},
    {'loss': 2.2016, 'grad_norm': 30.24620246887207, 'learning_rate': 3.4000000000000007e-05, 'epoch': 4.6},
    {'loss': 2.1816, 'grad_norm': 29.87877655029297, 'learning_rate': 3.45e-05, 'epoch': 4.67},
    {'loss': 2.1022, 'grad_norm': 30.376232147216797, 'learning_rate': 3.5e-05, 'epoch': 4.73},
    {'loss': 2.0605, 'grad_norm': 27.191997528076172, 'learning_rate': 3.55e-05, 'epoch': 4.8},
    {'loss': 1.9702, 'grad_norm': 27.74502944946289, 'learning_rate': 3.6e-05, 'epoch': 4.87},
    {'loss': 1.9598, 'grad_norm': 26.69854736328125, 'learning_rate': 3.65e-05, 'epoch': 4.93},
    {'loss': 2.0463, 'grad_norm': 25.799449920654297, 'learning_rate': 3.7e-05, 'epoch': 5.0},
    {'loss': 1.92, 'grad_norm': 25.425161361694336, 'learning_rate': 3.7500000000000003e-05, 'epoch': 5.07},
    {'loss': 1.9071, 'grad_norm': 23.969419479370117, 'learning_rate': 3.8e-05, 'epoch': 5.13},
    {'loss': 1.8577, 'grad_norm': 23.5513973236084, 'learning_rate': 3.85e-05, 'epoch': 5.2},
    {'loss': 1.8578, 'grad_norm': 23.79353904724121, 'learning_rate': 3.9000000000000006e-05, 'epoch': 5.27},
    {'loss': 1.8309, 'grad_norm': 22.23126792907715, 'learning_rate': 3.9500000000000005e-05, 'epoch': 5.33},
    {'loss': 1.817, 'grad_norm': 19.755769729614258, 'learning_rate': 4e-05, 'epoch': 5.4},
    {'loss': 1.8634, 'grad_norm': 19.017757415771484, 'learning_rate': 4.05e-05, 'epoch': 5.47},
    {'loss': 1.8222, 'grad_norm': 18.92751693725586, 'learning_rate': 4.1e-05, 'epoch': 5.53},
    {'loss': 1.7178, 'grad_norm': 18.211713790893555, 'learning_rate': 4.15e-05, 'epoch': 5.6},
    {'loss': 1.627, 'grad_norm': 16.356334686279297, 'learning_rate': 4.2e-05, 'epoch': 5.67},
    {'loss': 1.695, 'grad_norm': 14.707646369934082, 'learning_rate': 4.25e-05, 'epoch': 5.73},
    {'loss': 1.6656, 'grad_norm': 15.287571907043457, 'learning_rate': 4.3e-05, 'epoch': 5.8},
    {'loss': 1.4445, 'grad_norm': 11.876264572143555, 'learning_rate': 4.35e-05, 'epoch': 5.87},
    {'loss': 1.5212, 'grad_norm': 11.354605674743652, 'learning_rate': 4.4000000000000006e-05, 'epoch': 5.93},
    {'loss': 1.468, 'grad_norm': 10.721542358398438, 'learning_rate': 4.4500000000000004e-05, 'epoch': 6.0},
    {'loss': 1.4969, 'grad_norm': 12.777170181274414, 'learning_rate': 4.5e-05, 'epoch': 6.07},
    {'loss': 1.2772, 'grad_norm': 12.933666229248047, 'learning_rate': 4.55e-05, 'epoch': 6.13},
    {'loss': 1.3912, 'grad_norm': 10.254033088684082, 'learning_rate': 4.600000000000001e-05, 'epoch': 6.2},
    {'loss': 1.3305, 'grad_norm': 7.554629802703857, 'learning_rate': 4.6500000000000005e-05, 'epoch': 6.27},
    {'loss': 1.3947, 'grad_norm': 7.495401859283447, 'learning_rate': 4.7e-05, 'epoch': 6.33},
    {'loss': 1.1834, 'grad_norm': 8.260666847229004, 'learning_rate': 4.75e-05, 'epoch': 6.4},
    {'loss': 1.1838, 'grad_norm': 8.93397045135498, 'learning_rate': 4.8e-05, 'epoch': 6.47},
    {'loss': 1.1402, 'grad_norm': 7.821136474609375, 'learning_rate': 4.85e-05, 'epoch': 6.53},
    {'loss': 1.1398, 'grad_norm': 6.516462326049805, 'learning_rate': 4.9e-05, 'epoch': 6.6},
    {'loss': 1.1498, 'grad_norm': 4.884432792663574, 'learning_rate': 4.9500000000000004e-05, 'epoch': 6.67},
    {'loss': 1.1449, 'grad_norm': 4.398116588592529, 'learning_rate': 5e-05, 'epoch': 6.73},
    {'loss': 0.8893, 'grad_norm': 5.711645126342773, 'learning_rate': 4.9e-05, 'epoch': 6.8},
    {'loss': 1.0346, 'grad_norm': 8.935051918029785, 'learning_rate': 4.8e-05, 'epoch': 6.87},
    {'loss': 0.7849, 'grad_norm': 8.042488098144531, 'learning_rate': 4.7e-05, 'epoch': 6.93},
    {'loss': 0.8706, 'grad_norm': 5.013166904449463, 'learning_rate': 4.600000000000001e-05, 'epoch': 7.0},
    {'loss': 1.011, 'grad_norm': 3.6648542881011963, 'learning_rate': 4.5e-05, 'epoch': 7.07},
    {'loss': 0.8684, 'grad_norm': 3.4622254371643066, 'learning_rate': 4.4000000000000006e-05, 'epoch': 7.13},
    {'loss': 0.7887, 'grad_norm': 4.300750732421875, 'learning_rate': 4.3e-05, 'epoch': 7.2},
    {'loss': 0.9337, 'grad_norm': 6.193939685821533, 'learning_rate': 4.2e-05, 'epoch': 7.27},
    {'loss': 0.9007, 'grad_norm': 10.389395713806152, 'learning_rate': 4.1e-05, 'epoch': 7.33},
    {'loss': 0.7549, 'grad_norm': 6.95593786239624, 'learning_rate': 4e-05, 'epoch': 7.4},
    {'loss': 0.8068, 'grad_norm': 3.770811080932617, 'learning_rate': 3.9000000000000006e-05, 'epoch': 7.47},
    {'loss': 0.6636, 'grad_norm': 2.674513816833496, 'learning_rate': 3.8e-05, 'epoch': 7.53},
    {'loss': 0.8218, 'grad_norm': 2.7662370204925537, 'learning_rate': 3.7e-05, 'epoch': 7.6},
    {'loss': 0.7495, 'grad_norm': 2.7824504375457764, 'learning_rate': 3.6e-05, 'epoch': 7.67},
    {'loss': 0.5923, 'grad_norm': 3.6634321212768555, 'learning_rate': 3.5e-05, 'epoch': 7.73},
    {'loss': 0.6145, 'grad_norm': 3.726330280303955, 'learning_rate': 3.4000000000000007e-05, 'epoch': 7.8},
    {'loss': 0.7708, 'grad_norm': 3.831472396850586, 'learning_rate': 3.3e-05, 'epoch': 7.87},
    {'loss': 0.6467, 'grad_norm': 2.4696972370147705, 'learning_rate': 3.2000000000000005e-05, 'epoch': 7.93},
    {'loss': 0.6618, 'grad_norm': 2.992119550704956, 'learning_rate': 3.1e-05, 'epoch': 8.0},
    {'loss': 0.5679, 'grad_norm': 2.269789218902588, 'learning_rate': 3e-05, 'epoch': 8.07},
    {'loss': 0.6985, 'grad_norm': 2.4509692192077637, 'learning_rate': 2.9e-05, 'epoch': 8.13},
    {'loss': 0.7063, 'grad_norm': 2.2027740478515625, 'learning_rate': 2.8000000000000003e-05, 'epoch': 8.2},
    {'loss': 0.5536, 'grad_norm': 2.4598188400268555, 'learning_rate': 2.7000000000000002e-05, 'epoch': 8.27},
    {'loss': 0.6331, 'grad_norm': 2.914362907409668, 'learning_rate': 2.6000000000000002e-05, 'epoch': 8.33},
    {'loss': 0.5039, 'grad_norm': 2.9853081703186035, 'learning_rate': 2.5e-05, 'epoch': 8.4},
    {'loss': 0.6717, 'grad_norm': 3.0822112560272217, 'learning_rate': 2.4e-05, 'epoch': 8.47},
    {'loss': 0.6626, 'grad_norm': 2.092810869216919, 'learning_rate': 2.3000000000000003e-05, 'epoch': 8.53},
    {'loss': 0.6362, 'grad_norm': 2.3706352710723877, 'learning_rate': 2.2000000000000003e-05, 'epoch': 8.6},
    {'loss': 0.4466, 'grad_norm': 1.9527971744537354, 'learning_rate': 2.1e-05, 'epoch': 8.67},
    {'loss': 0.6643, 'grad_norm': 2.359027147293091, 'learning_rate': 2e-05, 'epoch': 8.73},
    {'loss': 0.5076, 'grad_norm': 2.1087090969085693, 'learning_rate': 1.9e-05, 'epoch': 8.8},
    {'loss': 0.6434, 'grad_norm': 1.9636847972869873, 'learning_rate': 1.8e-05, 'epoch': 8.87},
    {'loss': 0.5629, 'grad_norm': 2.0773305892944336, 'learning_rate': 1.7000000000000003e-05, 'epoch': 8.93},
    {'loss': 0.4898, 'grad_norm': 1.9774304628372192, 'learning_rate': 1.6000000000000003e-05, 'epoch': 9.0},
    {'loss': 0.4976, 'grad_norm': 2.4350483417510986, 'learning_rate': 1.5e-05, 'epoch': 9.07},
    {'loss': 0.512, 'grad_norm': 2.5156044960021973, 'learning_rate': 1.4000000000000001e-05, 'epoch': 9.13},
    {'loss': 0.5387, 'grad_norm': 2.0135273933410645, 'learning_rate': 1.3000000000000001e-05, 'epoch': 9.2},
    {'loss': 0.5674, 'grad_norm': 2.4419405460357666, 'learning_rate': 1.2e-05, 'epoch': 9.27},
    {'loss': 0.5522, 'grad_norm': 2.010197162628174, 'learning_rate': 1.1000000000000001e-05, 'epoch': 9.33},
    {'loss': 0.4909, 'grad_norm': 2.382014036178589, 'learning_rate': 1e-05, 'epoch': 9.4},
    {'loss': 0.5791, 'grad_norm': 2.033363103866577, 'learning_rate': 9e-06, 'epoch': 9.47},
    {'loss': 0.5458, 'grad_norm': 2.277101516723633, 'learning_rate': 8.000000000000001e-06, 'epoch': 9.53},
    {'loss': 0.5318, 'grad_norm': 1.7422252893447876, 'learning_rate': 7.000000000000001e-06, 'epoch': 9.6},
    {'loss': 0.7496, 'grad_norm': 1.9961813688278198, 'learning_rate': 6e-06, 'epoch': 9.67},
    {'loss': 0.5357, 'grad_norm': 1.7510958909988403, 'learning_rate': 5e-06, 'epoch': 9.73},
    {'loss': 0.4741, 'grad_norm': 1.8189436197280884, 'learning_rate': 4.000000000000001e-06, 'epoch': 9.8},
    {'loss': 0.3898, 'grad_norm': 1.690512776374817, 'learning_rate': 3e-06, 'epoch': 9.87},
    {'loss': 0.5302, 'grad_norm': 1.926150918006897, 'learning_rate': 2.0000000000000003e-06, 'epoch': 9.93},
    {'loss': 0.5061, 'grad_norm': 1.8221473693847656, 'learning_rate': 1.0000000000000002e-06, 'epoch': 10.0}
]

# Extract epochs and loss values
epochs = [entry['epoch'] for entry in training_data]
losses = [entry['loss'] for entry in training_data]

# Create the plot
plt.figure(figsize=(12, 8))
plt.plot(epochs, losses, linewidth=2, color='#2E86AB', marker='o', markersize=3, alpha=0.8)

# Customize the plot
plt.title('Training Loss Over Epochs', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Epoch', fontsize=12)
plt.ylabel('Loss', fontsize=12)
plt.grid(True, alpha=0.3)

# Add some styling
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_color('#333333')
plt.gca().spines['bottom'].set_color('#333333')

# Set axis limits for better visualization
plt.xlim(0, 10.5)
plt.ylim(0, max(losses) * 1.1)

# Add annotations for key points
min_loss_idx = losses.index(min(losses))
min_loss_epoch = epochs[min_loss_idx]
min_loss_value = losses[min_loss_idx]

plt.annotate(f'Min Loss: {min_loss_value:.4f}\nEpoch: {min_loss_epoch:.2f}', 
             xy=(min_loss_epoch, min_loss_value), 
             xytext=(min_loss_epoch + 1, min_loss_value + 0.5),
             arrowprops=dict(facecolor='black', shrink=0.05),
                fontsize=10, color='black', bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

# Show the plot
plt.tight_layout()
plt.show()
# Save the plot as an image file
plt.savefig('training_loss_plot.png', dpi=300, bbox_inches='tight')