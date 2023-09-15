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

bool has_master(MTSClientWrapper client){
    return MTS_HasMaster(client.ptr);
}

bool should_filter_note(MTSClientWrapper client, int midinote, int midichannel){
    return MTS_ShouldFilterNote(client.ptr, midinote, midichannel);
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

int frequency_to_note(MTSClientWrapper client, double freq, int midichannel){
    return MTS_FrequencyToNote(client.ptr, freq, midichannel);
}

py::tuple frequency_to_note_and_channel(MTSClientWrapper client, double freq){
    char midichannel = 0;
    int note;
    note = MTS_FrequencyToNoteAndChannel(client.ptr, freq, &midichannel);
    return py::make_tuple(note, (int)midichannel);
}

const char *get_scale_name(MTSClientWrapper client){
    return MTS_GetScaleName(client.ptr);
}

void set_note_tuning(float frequency_in_hz, int midinote){
    MTS_SetNoteTuning(frequency_in_hz, midinote);
}

void set_note_tunings(py::list frequencies_in_hz){
    double f[128];
    for(int i = 0; i < 128; i++) {
        f[i] = frequencies_in_hz[i].cast<double>();
    }
    MTS_SetNoteTunings(f);
}

void filter_note(bool doFilter, int midinote, int midichannel){
    MTS_FilterNote(doFilter, midinote, midichannel);
}

void set_multi_channel(bool set, int midichannel){
    MTS_SetMultiChannel(set, midichannel);
}

void set_multi_channel_note_tunings(py::list frequencies_in_hz, int midichannel){
    double f[128];
    for(int i = 0; i < 128; i++) {
        f[i] = frequencies_in_hz[i].cast<double>();
    }
    MTS_SetMultiChannelNoteTunings(f, midichannel);
}

void set_multi_channel_note_tuning(float frequency_in_hz, int midinote, int midichannel){
    MTS_SetMultiChannelNoteTuning(frequency_in_hz, midinote, midichannel);
}

void filter_note_multi_channel(bool doFilter, int midinote, int midichannel){
    MTS_FilterNoteMultiChannel(doFilter, midinote, midichannel);
}

void clear_note_filter_multi_channel(int midichannel){
    MTS_ClearNoteFilterMultiChannel(midichannel);
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

PYBIND11_MODULE(_mtsespy, m)
{
    m.doc() = "Wrapper for ODDSound MTS-ESP C++ library";
    py::class_<MTSClientWrapper>(m, "MTSClient");
    m.def("register_client", &register_client, "Register MTS client");
    m.def("deregister_client", &deregister_client, "De-register MTS client");
    m.def("has_master", &has_master, "Check if client is connected to a master");
    m.def("should_filter_note", &should_filter_note, "Check if note should not be played");
    m.def("note_to_frequency", &note_to_frequency, "Convert midi note to frequency");
    m.def("retuning_in_semitones", &retuning_in_semitones, "Midi note retuning in semitones");
    m.def("retuning_as_ratio", &retuning_as_ratio, "Midi note retuning as ratio");
    m.def("frequency_to_note", &frequency_to_note, "Get note number whose pitch is closest to given frequency");
    m.def("frequency_to_note_and_channel", &frequency_to_note_and_channel, "Get note number and midi channel for pitch closest to given frequency");
    m.def("get_scale_name", &get_scale_name, "Get scale name of current scale");
    m.def("register_master", &MTS_RegisterMaster, "Register MTS master");
    m.def("deregister_master", &MTS_DeregisterMaster, "Deregister MTS master");
    m.def("can_register_master", &MTS_CanRegisterMaster, "Check if master has already been registered");
    m.def("has_ipc", &MTS_HasIPC, "Check if process running master is using IPC");
    m.def("reinitialize", &MTS_Reinitialize, "Reset everything in MTS-ESP library");
    m.def("get_num_clients", &MTS_GetNumClients, "Get number of connected clients");
    m.def("set_note_tunings", &set_note_tunings, "Set tunings of all 128 midi notes");
    m.def("set_note_tuning", &set_note_tuning, "Set tuning of single note");
    m.def("set_scale_name", &MTS_SetScaleName, "Set scale name");
    m.def("filter_note", &filter_note, "Instruct clients to filter note");
    m.def("clear_note_filter", &MTS_ClearNoteFilter, "Clear note filter");
    m.def("set_multi_channel", &set_multi_channel, "Set whether MIDI channel is in multi-channel tuning table");
    m.def("set_multi_channel_note_tunings", &set_multi_channel_note_tunings, "Set tuning of all 128 notes on specific midi channel");
    m.def("set_multi_channel_note_tuning", &set_multi_channel_note_tuning, "Set tuning of note on specific midi channel");
    m.def("filter_note_multi_channel", &filter_note_multi_channel, "Instruct clients to filter note on specific midi channel");
    m.def("clear_note_filter_multi_channel", &clear_note_filter_multi_channel, "Clear note filter on specific midi channel");
    m.def("scala_files_to_frequencies", &scala_files_to_frequencies, "Build frequencies corresponding to given scala files");
}
