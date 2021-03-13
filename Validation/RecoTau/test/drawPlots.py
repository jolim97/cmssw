from ROOT import *
import os
import sys
gStyle.SetOptStat(kFALSE)

#fname1 = "DQM_V0001_R000000001__Global__CMSSW_X_Y_Z__RECO.root"
fname1 = "DQM_V0001_R000000001__Global__CMSSW_11_0_0__RECO.root"
fname2 = "DQM_V0001_R000000001__Global__CMSSW_11_0_0_pre13__RECO.root"

ZTTdir="DQMData/Run 1/RecoTauV/Run summary/miniAODValidation/ZTT/"
f1 = TFile(fname1)
f2 = TFile(fname2)
dir_antiids = ['vsJet','vsEle','vsMuo']
dir_wps = ['loose','medium','tight']
variables = ['_pt','_eta','_phi','_mass','_pu']
hists={}
c1 = TCanvas('c','c',800, 800)

plotpath = './plots'
if not os.path.isdir(plotpath):
    os.mkdir(plotpath)

for i in dir_antiids:
    for j in dir_wps:
        for k in variables:
            c1.cd()
            h1 = f1.Get(ZTTdir+i+'/'+j+'/tau_'+j+i+k)
            h2 = f2.Get(ZTTdir+i+'/'+j+'/tau_'+j+i+k)
            h1.SetLineColor(kRed)
            h2.SetLineColor(kBlue)
            m = max(h1.GetMaximum(), h2.GetMaximum())
            h1.SetMaximum(m*1.2)
            h1.Draw()
            h2.Draw("same")
            leg = TLegend(0.6, 0.8, 0.8, 0.89)
            leg.AddEntry(h1,'CMSSW_11_0_0', 'l')
            leg.AddEntry(h2,'CMSSW_11_0_0_pre13','l')
            leg.SetBorderSize(0)
            leg.SetTextSize(0.025)
            leg.Draw()
            c1.Print('./plots/'+"ZTTtau_"+j+i+k+'CMSSW_11_0_0_vs_CMSSW_11_0_0_pre13.pdf')

