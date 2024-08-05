
from django.shortcuts import render,HttpResponse
from .forms import FileForm
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import io
import base64,urllib
# Create your views here.

def histogram(datas,num_columns):

    plot_urls = {}
    for column in num_columns:
        sns.histplot(datas[column], bins=15, kde=True)
        plt.xlabel(column)
        plt.title(f'Histogram of {column}')

        buf = io.BytesIO()
        plt.savefig(buf,format='png')
        buf.seek(0)
        plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')
        # print(plot_url)
        plot_urls[column] = plot_url

    return plot_urls
def forms(request):
    if request.method == "POST":
        form = FileForm(request.POST,request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            dataset = pd.read_csv(file)

            num_columns = dataset.select_dtypes(include='number').columns
            med = dataset[num_columns].median()
            mean = dataset[num_columns].mean()
            std = dataset[num_columns].std()

            details = pd.DataFrame([med, mean, std])
            details.index = ["Median", "Mean", "Std"]

            few_rows = dataset.head().to_html()
            summary_statistics = details.to_html()
            null_values = dataset.isnull().sum()

            plots = histogram(dataset,num_columns)
            # print(plots)

            context = {"dataset" : dataset,"few_rows" : few_rows,"summary_statistics" : summary_statistics,
                       "null_values": null_values.to_frame().to_html(),"plots" : plots}

            return render(request,"app/display.html",context)
    form = FileForm()
    context = {"form":form}
    return render(request,'app/form.html',context)
