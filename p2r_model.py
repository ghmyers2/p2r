import time
import pandas as pd
import numpy as np
import lib.createInput as input
import lib.rtcOutput as rtOut
import os
# os.path.join("/home/accurt/rt_code/snow/")
import snowBranchConfig as config
from lmfit import Parameters
import lib.scatteringFiles as scat
from LUT.interpScatMatr import interpScatProp as interp
import matplotlib.pyplot as plt


def prepare_snow_iop(ar, d, reff, f_col, wl):
    ## interpolate and mix to get the snow IOP
    # ar: aspect ratio for columns
    # d: roughness parameter
    # reff: effective radius in microns
    # f_col: the fraction of columns in the mixture

    # interpolate to get the IOP for columns
    interpolant_1 = [ar, d, reff]
    c = interp(config.scatt_dir_dict[wl], wl, interpolant_1)
    ssc_prop_interp_arr_col, scattering_matrix_interp_arr_col = c.interp_NDLinear()

    # interpolate to get the IOP for plates
    interpolant_2 = [1. / ar, d, reff]
    c = interp(config.scatt_dir_dict[wl], wl, interpolant_2)
    ssc_prop_interp_arr_pla, scattering_matrix_interp_arr_pla = c.interp_NDLinear()

    # mix the IOPs with given f_col
    ssc_prop_arr = f_col * np.array(ssc_prop_interp_arr_col) + \
                   (1. - f_col) * np.array(ssc_prop_interp_arr_pla)
    ssc_prop_arr = list(ssc_prop_arr)

    scattering_matrix_arr = []
    for i in range(len(scattering_matrix_interp_arr_col)):
        scattering_matrix_element = f_col * scattering_matrix_interp_arr_col[i] + \
                                    (1. - f_col) * scattering_matrix_interp_arr_pla[i]
        scattering_matrix_arr.append(scattering_matrix_element)

    scatt_angles = c.scatt_angles

    return ssc_prop_arr, scatt_angles, scattering_matrix_arr


class infoParam:
    # The arrays in the config folder are indexed by "signatures" that describe them
    info_signatures = {"ar": config.arArr, "d": config.dArr, "f": config.fArr, "reff": config.A,
                            "vareff": config.B, "nr": config.NR,
                                "ni": config.NI, "aeroAmount": config.SPECIES_AMOUNT, "soot":config.soot}


    def __init__(self, sig, val, indices):
        self.paramSig = sig
        self.paramVal = val
        self.indices = indices

    def updateParamForInfoFile(self):

        # If the given parameter only requires a single index (the second index is set to None) i.e.
        # Effective radius of the first type of aerosol (A), etc.
        if self.indices[1] is None:
            # The values for the arrays are updated in the config folder
            self.info_signatures[self.paramSig][self.indices[0]] = self.paramVal

        # If that given parameter requires two indices to describe (the second index is NOT set to None) i.e.
        # Amount of aerosol type 2 in the 3rd atmospheric layer, etc.
        else:
            if self.paramSig == "nr" or self.paramSig == "ni":
                # The values for the arrays are updated in the config folder
                wl_list_str = list(config.active_lambda_names)
                wl_index = wl_list_str.index(self.indices[1])
                self.info_signatures[self.paramSig][self.indices[0] + config.NLAM*wl_index] = self.paramVal
            else:
                self.info_signatures[self.paramSig][self.indices[0]][self.indices[1]] = self.paramVal

    def setParamValue(self, curVal):
        # Updates the value of the parameter to a "current value" i.e. the value at that step in the iteration of the
        # inversion scheme
        self.paramVal = curVal



class p2r_model:


    # DESIGN THIS CLASS TO BE PARALLELIZED ON DIFFERENT PIXELS WITH DIFFERENT INITIAL GUESS ETC.
    # COPY EXECUTABLES INTO DIFFERENT FOLDERS RUNNING INDEPENDENTLY WITH DIFFERENT INFO FILES
    #
    # PROCESS ID IS A RUNTIME IDENTIFICATION (SOFTWARE - SENSE), MAX NUMBER OF UNIQUE PROCESS IDs IS EQUAL TO TOTAL NUMBER OF
    # PROCESSORS

        # df_param_guess = pd.Dataframe(columns=['the', 'free', 'params', 'you', 'need'])  ## make your first guess here
        # infoParamList = [infoParam(sig = "ar", val = 1.0, indices=(0,None)), infoParam(sig = "aeroAmount", val = 0.35, indices=(0,2)),
        #                       infoParam(sig = "srfNR", val = 1.2, indices = (1, None))]
        #


    def __init__(self, yList):
        self.y_list = yList
        pass


    def model_predict(self, param_pred, infoParamList, index, columns):


        # Update the values in the snowBranchConfig.py to the new current values prior to interpolating the
        # scattering matrices on the new values and running the RTC
        for col in param_pred.columns:
            CurParamVal  = param_pred.iloc[0][col]
            indexOfParam = list(param_pred.columns).index(col)
            infoParam    = infoParamList[indexOfParam]
            infoParam.setParamValue(CurParamVal)
            infoParam.updateParamForInfoFile()

        #### Preparing scattering matrix files for each of the wavelengths
        for i in range(len(config.ALAM)):
            wl = config.ALAM[i]
            ar_1, d_1, reff_1, f_1 = config.arArr[0], config.dArr[0], config.A[1], config.fArr[0]
            ssc_prop_arr, scatt_angles, scattering_matrix_arr = prepare_snow_iop(ar_1, d_1, reff_1, f_1, wl)
            output_dir = '/home/accurt/rt_code/rt_code/info/'
            output_name_1 = f"snow_iop_1_model_predict_{wl}.txt"
            snow_iop_1_name = output_dir + output_name_1
            interp.write_snow_ssc_prop(snow_iop_1_name, ssc_prop_arr, scatt_angles, scattering_matrix_arr, Reff=reff_1,
                                       NR=config.REFRAC_INDEX_DICT[wl][0], NI = config.REFRAC_INDEX_DICT[wl][1], Lambda=wl)

            ar_2, d_2, reff_2, f_2 = config.arArr[1], config.dArr[1], config.A[2], config.fArr[1]
            ssc_prop_arr, scatt_angles, scattering_matrix_arr = prepare_snow_iop(ar_2, d_2, reff_2, f_2, wl)

            output_name_2 = f"snow_iop_2_model_predict_{wl}.txt"
            snow_iop_2_name = output_dir + output_name_2

            interp.write_snow_ssc_prop(snow_iop_2_name, ssc_prop_arr, scatt_angles, scattering_matrix_arr, Reff=reff_2,
                                       NR=config.REFRAC_INDEX_DICT[wl][0], NI = config.REFRAC_INDEX_DICT[wl][1], Lambda=wl)
            imp = scat.getIOPs.sizedis_spher(config.mu, config.sigma)
            soot_1, soot_2 = config.soot[0], config.soot[1]
            # print("SOOOOT", soot_1, soot_2)
            tau_soot_2 = scat.getIOPs.calcTau_imp(imp, soot_2, config.rho_snow, config.rho_imp, wl , config.nr_imp, config.ni_imp, config.dep_2)
            tau_soot_1 = scat.getIOPs.calcTau_imp(imp, soot_1, config.rho_snow, config.rho_imp, wl , config.nr_imp, config.ni_imp, config.dep_1)

            # The snow_iop files must be places at the correct indices (dependent on the index of the current wavlength)
            # inside the config to correctly populate the .info file
            config.SCATTERING_FILENAME[config.NTYPE*i + 1] = snow_iop_2_name
            config.SCATTERING_FILENAME[config.NTYPE*i + 2] = snow_iop_1_name

            config.SPECIES_AMOUNT[0][0] = tau_soot_2

            config.SPECIES_AMOUNT[0][1] = tau_soot_1

            config.SPECIES_AMOUNT[1][0] = scat.calcTau(snow_iop_2_name, config.rho_snow, config.dep_2)
            config.SPECIES_AMOUNT[2][1] = scat.calcTau(snow_iop_1_name, config.rho_snow, config.dep_1)

        # Initializing instance of the info class with updated values from the snowBranchConfig.py
        infoFile = input.Atmo(config.MCAP, config.NCAP, config.NCAP2, config.MTOT, config.N3BY3, config.QSTOP,
                              config.QSTOP2, config.ERRBNDR, config.ERRBNDP, config.IGAUSS, config.IPRT, config.IREMV,
                              config.R1, config.R2, config.ALBEDO, config.SURFACE_FILENAME, config.OUTPUT_FILENAME,
                              config.SCATTERING_FILENAME, config.NTAU, config.NTAU2, config.nPhi, config.nGauss,
                              config.NPERS, config.NTYPE, config.NLAM, config.NLAYER, config.NGAS, config.A, config.B,
                              config.NSD, config.mu0, config.phi, config.ALAM, config.NR, config.NI, config.SPECIES_AMOUNT,
                              config.TAUABS, config.DELP)

        info_file_name = "modelPredictInfo.info"
        info_file_dir = "/home/accurt/rt_code/rt_code/info/"

        # Writing the info file
        infoFile.createAtmo(totalName = info_file_dir + info_file_name)
        os.chdir(config.rt_dir)
        os.system("make all")
        os.system("./vec_generate_obs info/modelPredictInfo.info 0 " + str(config.TAUREP))
        # os.remove(info_file_dir + info_file_name)

        # how would you like the output of the RT run to be structured???
        I_out = []
        Q_out = []
        U_out = []

        for j in range(len(config.OUTPUT_FILENAME)):
            # Putting each
            file = config.OUTPUT_FILENAME[j]
            modelOut = rtOut.rtcOutput(config.rt_dir + file + ".rsp")
            I_out.append([modelOut.RV11[i] + modelOut.RZ11[i] for i in range(len(modelOut.RV11))])
            Q_out.append([modelOut.RV21[i] + modelOut.RZ21[i] for i in range(len(modelOut.RV21))])
            U_out.append([modelOut.RV31[i] + modelOut.RZ31[i] for i in range(len(modelOut.RV31))])

        plt.show()
        rows = config.active_lambda_names
        zipped = list(zip(rows, I_out, Q_out, U_out))
        df = pd.DataFrame(zipped, columns=['wl', 'I', 'Q', 'U'])

        return df






if __name__=="__main__":
    # This is a test of the p2r_model.modelpredict function
    # 
    # PLEASE NOTE:
    #           IT IS INCREDIBLY IMPORTANT THAT THE ORDER OF THE infoParam OBJECTS IN THE infoparamList
    #           MATCHES THE ORDER THE PARAMETERS ARE ADDED TO TO THE lmfit.Parameters list (SEE BELOW)

    infoParamList = [infoParam(sig="soot", val=10.357, indices=(0, None)),
                     infoParam(sig="aeroAmount", val=3E-2, indices=(3, 1)),
                     infoParam(sig="nr", val=1.17, indices=(4, '470')),
                     infoParam(sig="vareff", val=0.75, indices=(1, None))]
    params = Parameters()
    params.add("aeroAmountlayer1type2", value = 10.357, min = 0.0, max = 11.0)
    params.add("aeroAmountLayer1Coarse", value = 3E-2, min = 0.0, max = 6E3)
    params.add("NRtype4wl470", value = 5.17, min = 0.0, max = 61.9)
    params.add("varefftype2", value = 0.75, min = 0.0, max = 0.85)
    l = list()
    v = list()
    for item in params:
        l.append(params[item].name)
        v.append(params[item].value)

    v = np.vstack(v)
    param_pred = pd.DataFrame(v.transpose(), columns = l)

    p2r = p2r_model(yList=list(param_pred.columns))
    out = p2r.model_predict(param_pred = param_pred, infoParamList=infoParamList, index='', columns='')
    print(out)
    quit()
