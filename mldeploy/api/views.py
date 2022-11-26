from django.core.files.storage import FileSystemStorage
from skimage.io import imread
import pickle
from skimage.transform import resize
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes


model = pickle.load(open('./models/model.h5', 'rb'))


@parser_classes((MultiPartParser, ))
class PredictImage(APIView):

    def post(self, request, format=None):
        disease_about = {
            'leafblast': ["Symptoms of rice blast are caused by the fungus Magnaporthe grisea, which is one of the most destructive diseases of rice. The fungus can survive on the straw after harvest and thus be carried over to the next season. The disease is favored by cool temperatures, frequent rainfalls, and low soil moisture. A prolonged period of leaf moisture is also required for infection. Finally, plants sown in soils with high nitrogen or low silicon levels are more likely to develop the disease.",
                          "Chemical treatment is the most effective way to solve eradicate the blast disease. Seed treatment with thiram is effective against the disease. Fungicides containing azoxystrobin, or active ingredients of the family of triazoles or strobilurins can also be sprayed at nursery, tillering and panicle emergence stages to control rice blast. One or two fungicide applications at heading can be effective in controlling the disease.", ],
            'brownspot': ["The symptoms are caused by the fungus, Cochliobolus miyabeanus. It can survive in seeds for more than four years and spread from plant to plant through airborne spores. Infected plant debris left in the field and weeds are other common ways to spread the disease. High humidity (86-100%), prolonged periods of leaf moisture and high temperatures (16-36°C) are very favorable for the fungi. The disease often occurs in fields with mismanagement of soil fertility, mainly in terms of micronutrients.",
                          "Before planting treat seed with hot water: 53-54°C for 10-12 minutes. During growth ensure that plants have correct nutrition: apply fertilizer at recommended rates. After harvest collect straw and other debris after harvest and burn it with the stubble, or plough everything into the soil. For chemical control IRRI recommends seed treatments with iprodione, stilburins (azoxystrobin or trifloxystrobin), azole (propiconazole), or carbendazin fungicides.", ],
            'hispa': ["Damage is caused by the adults and larvae of the rice hispa, Dicladispa armigera. Adult beetles scrape the upper surface of leaf blades leaving only the lower layer. It feeds inside the leaf tissue by mining along the leaf axis, and subsequently pupates internally. Grassy weeds, heavy fertilization, heavy rains and high relative humidity favor rice hispa infestation. Rice field appears burnt when severely infested.",
                      "A cultural control method that is recommended for the rice hispa is to avoid over fertilizing the field. Close plant spacing results in greater leaf densities that can tolerate higher hispa numbers. To prevent egg laying of the pests, the shoot tips can be cut. Among the biological control agents, there are small wasps that attack the eggs and larvae. A reduviid bug eats upon the adults. There are three fungal pathogens that attack the adults. For chmeical control following ingredients is recommended: chlorpyriphos, malathion, cypermethrin, fenthoate.", ],
            'healthy': ["NA",
                        "NA", ],
        }
        fileObj = request.FILES['image']
        fs = FileSystemStorage()
        filePathName = fs.save(fileObj.name, fileObj)
        filePathName = fs.url(filePathName)
        testimage = '.'+filePathName
        img = imread(testimage)
        img_resize = [resize(img, (150, 150, 3)).flatten()]
        Categories = ['healthy', 'leafblast', 'hispa', 'brownspot']
        probability = model.predict_proba(img_resize)
        for ind, val in enumerate(Categories):
            print(f'{val} = {probability[0][ind]*100}%')
        res_index = model.predict(img_resize)[0]
        res_disease = Categories[res_index]
        print("The predicted image is : " + res_disease)
        context = {
            'filePathName': filePathName,
            'predictedLabel': res_disease,
            'index': str(res_index),
            'about': disease_about[res_disease],
        }
        return JsonResponse(context)

    def get(request):
        data = {"Name": "Roshan"}
        return JsonResponse(data)
