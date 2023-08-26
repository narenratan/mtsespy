#include <pybind11/pybind11.h>
#include "libMTSClient.h"
#include "libMTSMaster.h"
#include "Tunings.h"

namespace py = pybind11;

struct MTSClientWrapper {
    MTSClient *ptr;
};

MTSClientWrapper register_client(){
    MTSClient* m = MTS_RegisterClient();
    return MTSClientWrapper{m};
}

void deregister_client(MTSClientWrapper client){
    MTS_DeregisterClient(client.ptr);
}

double note_to_frequency(MTSClientWrapper client, int midinote, int midichannel){
    return MTS_NoteToFrequency(client.ptr, midinote, midichannel);
}

double retuning_in_semitones(MTSClientWrapper client, int midinote, int midichannel){
    return MTS_RetuningInSemitones(client.ptr, midinote, midichannel);
}

double retuning_as_ratio(MTSClientWrapper client, int midinote, int midichannel){
    return MTS_RetuningAsRatio(client.ptr, midinote, midichannel);
}

void set_note_tuning(float frequency_in_hz, int midinote){
    MTS_SetNoteTuning(frequency_in_hz, midinote);
}

void set_multi_channel(bool set, int midichannel){
    MTS_SetMultiChannel(set, midichannel);
}

void set_multi_channel_note_tuning(float frequency_in_hz, int midinote, int midichannel){
    MTS_SetMultiChannelNoteTuning(frequency_in_hz, midinote, midichannel);
}

py::list scala_files_to_frequencies(std::string scl_filename, std::string kbm_filename){
    auto s = Tunings::readSCLFile(scl_filename);
    auto k = Tunings::readKBMFile(kbm_filename);

    Tunings::Tuning t(s, k);

    py::list res;
    for(int i = 0; i < 128; i++) {
        res.append(t.frequencyForMidiNote(i));
    }
    return res;
}

PYBIND11_MODULE(mtsespy, m)
{
    m.doc() = "Wrapper for ODDSound MTS-ESP C++ library";
    py::class_<MTSClientWrapper>(m, "MTSClient");
    m.def("register_client", &register_client, "Register MTS client");
    m.def("deregister_client", &deregister_client, "De-register MTS client");
    m.def("note_to_frequency", &note_to_frequency, "Convert midi note to frequency");
    m.def("retuning_in_semitones", &retuning_in_semitones, "Midi note retuning in semitones");
    m.def("retuning_as_ratio", &retuning_as_ratio, "Midi note retuning as ratio");
    m.def("can_register_master", &MTS_CanRegisterMaster, "Check if master has already been registered");
    m.def("register_master", &MTS_RegisterMaster, "Register MTS master");
    m.def("deregister_master", &MTS_DeregisterMaster, "Deregister MTS master");
    m.def("set_note_tuning", &set_note_tuning, "Set tuning of single note");
    m.def("set_multi_channel", &set_multi_channel, "Set whether MIDI channel is in multi-channel tuning table");
    m.def("set_multi_channel_note_tuning", &set_multi_channel_note_tuning, "Set tuning of note on specific midi channel");
    m.def("scala_files_to_frequencies", &scala_files_to_frequencies, "Build frequencies corresponding to given scala files");
}
