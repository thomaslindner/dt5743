#include "TDT743Waveform.h"

#include "TDT743RawData.hxx"
#include "TDirectory.h"


/// Reset the histograms for this canvas
TDT743Waveform::TDT743Waveform(){

  SetSubTabName("DT743 Waveforms");
  SetUpdateOnlyWhenPlotted(true);
  
  CreateHistograms();

}


void TDT743Waveform::CreateHistograms(){

  // check if we already have histogramss.
  char tname[100];
  sprintf(tname,"DT743_%i",0);

  TH1D *tmp = (TH1D*)gDirectory->Get(tname);
  if (tmp) return;

  int fWFLength = 200; // Need a better way of detecting this...
  int numSamples = fWFLength / 1;
  
  // Otherwise make histograms
  clear();
  
  for(int i = 0; i < 8; i++){ // loop over 2 channels
    
    char name[100];
    char title[100];
    sprintf(name,"DT743_%i",i);
    
    sprintf(title,"DT743 Waveform for channel=%i",i);	
    
    TH1D *tmp = new TH1D(name, title, numSamples, 0, fWFLength);
    tmp->SetXTitle("ns");
    tmp->SetYTitle("ADC value");
    
    push_back(tmp);
  }
  std::cout << "TDT743Waveform done init...... " << std::endl;
  
}


void TDT743Waveform::UpdateHistograms(TDataContainer& dataContainer){
  
  int eventid = dataContainer.GetMidasData().GetEventId();
  int timestamp = dataContainer.GetMidasData().GetTimeStamp();
  
  TDT743RawData *dt743 = dataContainer.GetEventData<TDT743RawData>("43FS");
  
  if(dt743){      
    
    
    std::vector<RawChannelMeasurement> measurements = dt743->GetMeasurements();
    
    // Need to change timebase and number of samples!!!

    for(int i = 0; i < measurements.size(); i++){
      
      int chan = measurements[i].GetChannel();
      
      
      // Reset the histogram...
      for(int ib = 0; ib < GetHistogram(chan)->GetNbinsX(); ib++)
	GetHistogram(chan)->SetBinContent(ib+1,0);
      
      //std::cout << "Nsamples " <<  measurements[i].GetNSamples() << std::endl;
      for(int ib = 0; ib < measurements[i].GetNSamples(); ib++){
	GetHistogram(chan)->SetBinContent(ib+1, measurements[i].GetSample(ib));
      }
      
    }
  }
  
}



void TDT743Waveform::Reset(){
  
  
  for(int i = 0; i < 8; i++){ // loop over channels
    int index =  i;
    
    // Reset the histogram...
    for(int ib = 0; ib < GetHistogram(index)->GetNbinsX(); ib++) {
      GetHistogram(index)->SetBinContent(ib, 0);
    }
    
    GetHistogram(index)->Reset();
    
  }
}
