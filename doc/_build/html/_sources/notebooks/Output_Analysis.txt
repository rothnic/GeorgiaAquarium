
.. code:: python

    import numpy as np
    from numpy.random import randn
    import pandas as pd
    from scipy import stats
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    %matplotlib inline
.. code:: python

    sns.set_palette("deep", desat=.6)
    sns.set_context(rc={"figure.figsize": (8, 4)})
.. code:: python

    data = pd.read_csv('cases_2014-07-03_21-25-07.csv', usecols=["um.pedsPerHourOff","um.pedsPerHourOn"])
.. code:: python

    data = data.dropna()
    data.head()



.. raw:: html

    <div style="max-height:1000px;max-width:1500px;overflow:auto;">
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>um.pedsPerHourOff</th>
          <th>um.pedsPerHourOn</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1</th>
          <td> 141.836735</td>
          <td>  509.183673</td>
        </tr>
        <tr>
          <th>3</th>
          <td> 662.244898</td>
          <td>  907.142857</td>
        </tr>
        <tr>
          <th>5</th>
          <td> 539.795918</td>
          <td>  447.959184</td>
        </tr>
        <tr>
          <th>7</th>
          <td> 631.632653</td>
          <td> 1152.040816</td>
        </tr>
        <tr>
          <th>9</th>
          <td> 417.346939</td>
          <td>  356.122449</td>
        </tr>
      </tbody>
    </table>
    <p>5 rows × 2 columns</p>
    </div>



.. code:: python

    sns.kdeplot(data['um.pedsPerHourOff'], shade=True);
    sns.kdeplot(data['um.pedsPerHourOn'], shade=True);


.. image:: \notebooks\Output_Analysis_files\Output_Analysis_4_0.png

